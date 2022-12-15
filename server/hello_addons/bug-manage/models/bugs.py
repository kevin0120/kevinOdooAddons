# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Bug(models.Model):
    _name = 'bm.bug'
    _description = 'bug'
    name = fields.Char('bug简述', required=True)
    detail = fields.Text()
    is_closed = fields.Boolean('是否关闭')
    close_reason = fields.Selection([('changed', '已修改'), ('cannot', '无法修改'), ('delay', '推迟')], string='关闭理由')
    user_id = fields.Many2one('res.users', string='负责人')
    follower_id = fields.Many2many('res.partner', string='关注者')

    @api.model
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
