from webmother.passport import Passport
from tweb.license import License
from webmother.service import ctrl_passport

system_name = 'product'

max_lic_text = 'product:111111111;30;'
profiles = {
    'product': {
        'switch': [
            "create",
            "read",
            "update",
            "remove",
            "submit",
            "audit",
            "reject",
            "activate",
            "deactivate"
        ],
        'number': [
            "visible_level"  # 资源可见级别，越大表示可以看到status值更低的资源，取值范围为资源status取值范围，如0～40
        ],
    }
}
display = {
    'zh': {
        'product': '产品管理',
        'product.switch': '权限开关',
        'product.switch.create': '创建',
        'product.switch.read': '读取',
        'product.switch.update': '更新',
        'product.switch.remove': '移除',
        'product.switch.submit': '提交',
        'product.switch.audit': '审核',
        'product.switch.reject': '驳回',
        'product.switch.activate': '上架',
        'product.switch.deactivate': '下架',
        'product.number': '数量限制',
        'product.number.visible_level': '可见级别',
    },
    'en': {
        'product': 'Product Manage',
        'product.switch': 'Switches',
        'product.switch.create': 'Create',
        'product.switch.read': 'Read',
        'product.switch.update': 'Update',
        'product.switch.remove': 'Remove',
        'product.switch.submit': 'Submit',
        'product.switch.audit': 'Audit',
        'product.switch.reject': 'Reject',
        'product.switch.activate': 'Activate',
        'product.switch.deactivate': 'Deactivate',
        'product.number': 'Number Limit',
        'product.number.visible_level': 'Visible Level',
    }
}


def append_extra():
    # 添加本系统涉及到的权限项
    Passport.add_system_profile(system_name, profiles, display)

    # 更新超级管理员的账户相关权限
    extra_lic = License(profiles, display).parse(max_lic_text)
    ctrl_passport.simple_update('0', '0', extra_lic.json)
