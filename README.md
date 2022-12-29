# go releaser
### odoo 脚手架
```bash
scaffold bug-manage hello_addons

前端 owl框架 jquery ajax rpc

python Gevent

https://www.cnblogs.com/ygj0930/p/10826114.html
```

### odoo 用户和用户组
```bash
https://www.cnblogs.com/watermeloncode/p/15767902.html
# Odoo14 groups && rule

# admin账户以及权限的来源：
# admin创建代码在：odoo/odoo/addons/base/data/res_users_data.xml中
<data noupdate="1">
<!-- user 1 is the technical admin user -->
<record model="res.users" id="base.user_root">
    <field name="partner_id" ref="base.partner_root"/>
    <field name="company_id" ref="main_company"/>
    <field name="company_ids" eval="[(4, ref('main_company'))]"/>
    <field name="email">root@example.com</field>
    <field name="signature"><![CDATA[<span>-- <br/>
System</span>]]></field>
</record>

<!-- user 2 is the human admin user -->
<record id="user_admin" model="res.users">
    <field name="login">admin</field>
    <field name="password">admin</field>
    <field name="partner_id" ref="base.partner_admin"/>
    <field name="company_id" ref="main_company"/>
    <field name="company_ids" eval="[(4, ref('main_company'))]"/>
    # 注意这里：groups_id字段会关联的就是权限组，这里初始化的时候会将权限组清空一遍
    <field name="groups_id" eval="[(6,0,[])]"/>
    <field name="image_1920" type="base64" file="base/static/img/avatar_grey.png"/>
    <field name="signature"><![CDATA[<span>-- <br/>
Administrator</span>]]></field>
</record>
</data>
# noupdate="1"
# 只有在安装的时候会执行data中的代码
# 如果noupdate="0"或者没设置的话，安装升级的时候都会执行data中的代码
# 另一种情况是-i modelname的时候不管noupdate设置的啥都会执行data代码

# 当我们在.py的model中增加字段的时候，我们经常需要./odoo-bin -c odoo.cfg -i base来初始化字段，否则会报错
# 这时候时候携带的 -i base参数，会导致data中的代码重新执行一遍初始化
# 因为groups_id字段值被清空了，所以导致给admin设置的权限被初始化了
# 如何解决这个问题：那就是不加-i


# 权限组(res.groups)的作用：
# 1.限制用户models的增删改查(通过.csv来编写)
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_login_image,access_login_image,model_login_image,,1,1,1,1
# 2.控制按钮的显示隐藏
<button name="open" string="Join Video Meeting" type="object" class="oe_highlight" groups='base.group_no_one'/>
# 3.控制menu菜单的显示隐藏
<menuitem action='payment_token_action' id='payment_token_menu' parent='account.root_payment_menu' groups='base.group_no_one'/>
# 4.控制fields的显示隐藏
invoice_amount = fields.Boolean(groups='account.group_account_invoice,account.group_account_readonly')
# 权限组如何声明：
<record id="group_ship_support_contact_us_menu" model="res.groups" >
    <field name="name">Contact Us</field>
    # category_id的值来自__manifast__.py的category值。"base.module_category_"是前缀加上category的值(需要将非字母数字下划线的值替换成下划线)
    <field name="category_id" ref="base.module_category_ship_support"/>
    # users哪些用户默认拥有这些权限
    <field name="users" eval="[(4, ref('base.user_admin'))]"/>
    # implied_ids继承其他组。这样其他组拥有的权限都会自带过来
    <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
</record>


# 过滤域(ir.rule)的作用是：用户访问models的时候强制加上domain过滤条件。过滤域是附加在权限组中的
<record id="account_move_line_rule_group_readonly" model="ir.rule">
    <field name="name">Readonly Move Line</field>
    # model_id：模块标识符，"model_"前缀+模块名(点替换成下划线)
    <field name="model_id" ref="model_account_move_line"/>
    # domain_force：过滤domain
    <field name="domain_force">[(1, '=', 1)]</field>
    # groups：该过滤与作用于哪些权限组
    <field name="groups" eval="[(4, ref('account.group_account_readonly'))]"/>
    <field name="perm_write" eval="False"/>
    <field name="perm_create" eval="False"/>
    <field name="perm_unlink" eval="False"/>
</record>
```