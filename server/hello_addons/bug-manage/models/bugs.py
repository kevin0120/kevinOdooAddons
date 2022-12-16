# -*- coding: utf-8 -*-
from random import randint

from odoo import models, fields, api


class Bug(models.Model):
    _name = 'bm.bug'
    _description = 'bug'
    name = fields.Char('bug简述', required=True)
    detail = fields.Text()

    def _default_color(self):
        self.env.user.notify_info(f'field default', sticky=True)
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

    def do_close(self):
        for item in self:
            item.is_closed = True
        return True


class bug_manage(models.Model):
    _name = 'bug.manage'

    name = fields.Char(string="名称")
    value = fields.Integer(string="程度")
    value2 = fields.Float(string="百分比", compute="_value_pc", store=True)
    description = fields.Text(string="描述")

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
