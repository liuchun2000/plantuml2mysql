UML legend:

table = class
#pkey
+index


## 数据模型
```plantuml
entity cmdb_asset_category {
  资产分类
  ==
  #id int(11) not null '主键id'
  asset_category_type varchar(32) not null '资产类型,相同用途下唯一'
  asset_category_name varchar(64) not null '分类名称'
  asset_category_purpose tinyint(1) not null  '用途 0-设备 1-软件 2-虚拟机'
  asset_category_leaf tinyint(4) not null default 0 '是否叶子节点 0否 1是'
  asset_category_desc varchar(512) null '备注'
  asset_category_parent_id int(11) not null default0 '父分类id'
  asset_category_display_order int(6) not null default0 '显示顺序 从小到大'
}

entity cmdb_asset {
  资产
  ==
  #id int(11) not null '主键id'
  asset_type varchar(32) not null '资产类型 对应cmdb_asset_category的asset_category_type'
  asset_uuid varchar(64) null '资产唯一标识'
  asset_desc varchar(512) null '备注'
}

entity cmdb_asset_extend {
  资产扩展数据
  ==
  #id int(11) '主键id'
  +asset_id int(11) not null '资产id'
  +asset_extend_key varchar(64) not null 'key值'
  asset_extend_value mediumtext not null 'value值'
}

entity cmdb_asset_extend_template {
  资产扩展数据模板
  ==
  #id int(11) '主键id'
  asset_type varchar(32) not null '资产类型对应cmdb_asset_categor的asset_category_type'
  asset_extend_template_key varchar(64) not null 'key值'
  asset_extend_template_ui mediumtext not null '模板界面配置'
  asset_extend_template_data mediumtext not null '模板数据配置'
  asset_extend_template_excel mediumtext not null '模板Excel配置'
  asset_extend_template_alert mediumtext not null '模板告警配置'
  asset_extend_template_desc varchar(512) null '备注'
}
```