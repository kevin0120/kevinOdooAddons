# -*- coding: utf-8 -*-
import datetime
from datetime import time
from random import randint

from odoo import models, fields, api, _lt, _
from odoo.exceptions import UserError
from odoo.osv.expression import AND

SEARCH_PANEL_ERROR_MESSAGE = _lt("Too many items to display.")


def childofisindomain(domain=None):
    for i in range(len(domain)):
        domain1 = domain[i]
        if isinstance(domain1, list) and len(domain1) == 3 and domain1[0] == 'meeting_id' \
                and domain1[1] == 'child_of':
            return i
    return -1


def parentofisindomain(domain=None):
    for i in range(len(domain)):
        domain1 = domain[i]
        if isinstance(domain1, list) and len(domain1) == 3 and domain1[0] == 'meeting_id' \
                and domain1[1] == 'parent_of':
            return i
    return -1


class Bug(models.Model):
    _name = 'bm.bug'
    _description = 'bug'
    # _parent_name = 'meeting_id'
    name = fields.Char('bug简述', required=True)
    detail = fields.Text()

    def _default_color(self):
        self.env.user.notify_info('{} field default'.format(datetime.datetime.now()), sticky=True)
        return randint(1, 11)

    detail1 = fields.Char(string='detail1', default=_default_color,
                          compute='_compute_name')
    user_id = fields.Many2one('res.users', string='负责人')
    meeting_id = fields.Many2one('bug.manage', string='会议')

    is_closed = fields.Boolean('是否关闭')
    close_reason = fields.Selection([('changed', '已修改'), ('cannot', '无法修改'), ('delay', '推迟')], string='关闭理由')

    follower_id = fields.Many2many('res.partner', string='关注者')
    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]

    @api.onchange('user_id')
    def _onchange_user_id(self):
        self.env.user.notify_info(f'field onchange', sticky=True)
        for rec in self:
            rec.detail1 = "%s's opportunity" % rec.user_id.login

    @api.depends('user_id')
    def _compute_name(self):
        self.env.user.notify_info(f'field compute', sticky=True)
        for lead in self:
            if not lead.detail1 and lead.user_id and lead.user_id.name:
                lead.detail1 = "%s's opportunity" % lead.user_id.name

    @api.model
    def default_get(self, fields_list):
        res = super(Bug, self).default_get(fields_list)
        if 'model_object' in fields_list:
            res.update({
                'model_object': self.env['ir.model'].search(
                    [('model', '=', 'onesphere.tightening.result')]).id
            })
        if 'model_object_field' in fields_list:
            res.update({
                'model_object_field': self.env['ir.model.fields']._get_ids(
                    'onesphere.tightening.result').get('measurement_final_torque')
            })
        return res

    def convertchildofdomian(self, childofstring=""):
        par = childofstring.split("-")
        bugs = self.env['bm.bug'].search(['|', ('meeting_id', '=', None), ('meeting_id.room_id', '=', None)])
        if par[0] != "0":
            id1 = int(par[0])
            bugs = self.env['bm.bug'].search([('meeting_id.room_id', 'in', [id1])])
        if len(par) == 2:
            id2 = int(par[1])
            bugs = bugs.filtered(lambda l: l.meeting_id.id == id2)
        return bugs.ids

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        i = childofisindomain(domain)
        if i >= 0:
            bugs = self.convertchildofdomian(domain[i][2])
            domain_repalce = ['id', 'in', bugs]
            domain[i] = domain_repalce
        i = parentofisindomain(domain)
        if i >= 0:
            domain[i] = [1, '=', 1]
        return super(Bug, self).search_read(domain, fields, offset, limit, order)

    def read(self, fields=None, load='_classic_read'):
        views = super(Bug, self).read(fields=fields, load=load)
        return views

    def write(self, vals):
        views = super(Bug, self).write(vals)
        return views

    @api.model_create_multi
    def create(self, vals_list):
        views = super(Bug, self).create(vals_list)
        return views

    def unlink(self):
        views = super(Bug, self).unlink()
        return views

    def exists(self):
        ids = self._existing()
        existing = self.filtered(lambda rec: rec.id in ids)
        return existing

    @api.model
    def load_views(self, views, options=None):
        views = super(Bug, self).load_views(views, options)
        return views

    @api.model
    def search_panel_select_range(self, field_name, **kwargs):
        parent_name = 'parent_id'
        bugs = self.env['bm.bug'].search([('meeting_id', '=', False)]).ids
        field_range = {
            '0': {'id': '0',
                  'display_name': '未知产品',
                  'parent_id': False,
                  '__count': len(bugs)
                  },
            '0-0': {
                'id': '0-0',
                'display_name': '未知作业',
                'parent_id': '0',
                '__count': len(bugs)
            },
        }
        products = self.env['meeting.room'].search([])
        for product in products:
            field_range.update({
                str(product.id): {'id': str(product.id),
                                  'display_name': product.display_name,
                                  'parent_id': False,
                                  '__count': 0
                                  }
            })

            for operation in product.manage_ids:
                field_range.update({
                    str(product.id) + '-' + str(operation.id): {'id': str(product.id) + '-' + str(operation.id),
                                                                'display_name': operation.display_name,
                                                                'parent_id': str(product.id),
                                                                '__count': len(operation.bug_ids.ids)
                                                                },
                })
                field_range[str(product.id)]['__count'] += len(operation.bug_ids.ids)

        operations = self.env['bug.manage'].search([('room_id', '=', False)])

        for operation in operations:
            field_range.update({
                '0-' + str(operation.id): {
                    'id': '0-' + str(operation.id),
                    'display_name': operation.display_name,
                    'parent_id': '0',
                    '__count': len(operation.bug_ids.ids)
                },
            })
            field_range['0']['__count'] += len(operation.bug_ids.ids)

        return {
            'parent_field': parent_name,
            'values': list(field_range.values()),
        }

    def do_close(self):
        for item in self:
            item.is_closed = True
        return True


class bug_manage(models.Model):
    _name = 'bug.manage'
    # _parent_name = 'room_id'
    name = fields.Char(string="名称")
    value = fields.Integer(string="程度")
    value2 = fields.Float(string="百分比", compute="_value_pc", store=True)
    description = fields.Text(string="描述")
    bug_ids = fields.One2many('bm.bug', 'meeting_id', string='bug')
    room_id = fields.Many2one('meeting.room', string='会议室')

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        sr = super(bug_manage, self).search_read([], fields, offset, limit, order)
        return sr

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100


class meeting_room(models.Model):
    _name = 'meeting.room'
    name = fields.Char(string="名称")
    description = fields.Text(string="描述")
    manage_ids = fields.One2many('bug.manage', 'room_id', string='会议')
