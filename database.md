UML legend:

table = class
#pkey
+index


## Data Schema For CMDB
```plantuml
  entity app_system {
    应用系统
    ==
    #application_id int(11) NOT NULL AUTO_INCREMENT COMMENT '唯一自增id'
    system_name_id int(11) NOT NULL COMMENT '系统名称id来自分组'
    owning_system_id int(11) NOT NULL COMMENT '所属系统，数据字典'
    business_type_id int(11) DEFAULT NULL COMMENT '业务类型，数据字典'
    system_version varchar(20) DEFAULT NULL COMMENT '系统版本号'
    system_type enum('测试系统''生产系统') DEFAULT NULL COMMENT '测试系统、生产系统'
    current_status_id int(11) DEFAULT NULL COMMENT '当前状态id数据字典'
    update_date date DEFAULT NULL COMMENT '版本更新日期'
    system_online_time date DEFAULT NULL COMMENT '系统上线时间'
    system_logout_time date DEFAULT NULL COMMENT '系统下线时间'
    deploy_way_id int(11) DEFAULT NULL COMMENT '部署方式数据字典'
    access_address varchar(128) NOT NULL COMMENT '访问地址'
    network enum('内网''外网') DEFAULT NULL COMMENT '内网/外网'
    system_level_id int(11) DEFAULT NULL COMMENT '系统等级数据字典'
    construction_type_id int(11) DEFAULT NULL COMMENT '建设类型数据字典'
    software_ids varchar(256) DEFAULT NULL COMMENT '使用软件ids以逗号隔开'
    description varchar(256) DEFAULT NULL COMMENT '描述'
    intake_i6000_monitor tinyint(2) DEFAULT NULL COMMENT '是否纳入i6000监控'
    filing_in_i6000 tinyint(2) DEFAULT NULL COMMENT '是否在i6000备案'
    filing_code varchar(64) DEFAULT NULL COMMENT 'i6000备案编号'
    access_property_monitor tinyint(2) DEFAULT NULL COMMENT '是否接入性能检测'
    third_party_security_assessment tinyint(2) DEFAULT NULL COMMENT '第三方安全测评'
    evaluate_company_vendor_id int(11) DEFAULT NULL COMMENT '测评厂商'
    evaluate_report_code varchar(64) DEFAULT NULL COMMENT '测评报告编号'
    security_level_id int(11) DEFAULT NULL COMMENT '等级保护安全等级数据字典'
    security_level_evaluation_date date DEFAULT NULL COMMENT '等级保护测评日期'
    occupy_company_id int(11) DEFAULT NULL COMMENT '使用部门来自companyid'
    occupy_org_id int(11) DEFAULT NULL COMMENT '使用部门来自orgid'
    system_vendor_id int(11) DEFAULT NULL COMMENT '系统实施厂商id'
    system_vendor_contacts varchar(20) DEFAULT NULL COMMENT '系统实施厂商联系方式'
    outsourcing_maintain_company_id int(11) DEFAULT NULL COMMENT '外委运维厂商来自companyid'
    outsourcing_maintain_org_id int(11) DEFAULT NULL COMMENT '外委运维厂商来自orgid'
    outsourcing_maintain_contacts_id int(11) DEFAULT NULL COMMENT '外委运维联系人id'
    outsourcing_maintain_contacts varchar(20) DEFAULT NULL COMMENT '外委运维联系人联系方式'
    business_charge_company_id int(11) DEFAULT NULL COMMENT '业务主管部门来自companyid'
    business_charge_org_id int(11) DEFAULT NULL COMMENT '业务主管部门来自orgid'
    business_director_id int(11) NOT NULL COMMENT '业务负责人id'
    business_director_contacts varchar(20) DEFAULT NULL COMMENT '业务负责人联系方式'
    maintain_company_id int(11) DEFAULT NULL COMMENT '运维部门来自companyid'
    maintain_org_id int(11) DEFAULT NULL COMMENT '运维部门来自orgid'
    maintainer_id int(11) NOT NULL COMMENT '运维责任人'
    maintainer_contacts varchar(20) DEFAULT NULL COMMENT '运维责任人联系方式'
  }

  entity app_system_group {
    业务系统分组
    ==
    #id int(11) NOT NULL AUTO_INCREMENT COMMENT '主键'
    group_name varchar(64) DEFAULT NULLCOMMENT '分组名称'
  }

  entity app_system_ldu {
    应用系统逻辑部署单元
    ==
    #ldu_id   int auto_increment
    +application_id    int    nullCOMMENT '应用系统ID'
    ldu_name  varchar(64)  null COMMENT '逻辑部署单元名称'
    ldu_type   varchar(64)  null COMMENT '组件类型'
    node_count  int(11)          null COMMENT '节点数量'
    ldu_nodes   varchar(512) null COMMENT 'ldu节点'
    cluster_id  varchar(32)  null COMMENT '集群id'
    type  tinyint      null COMMENT '0 集群 1 实例'
    description  varchar(256) null COMMENT '描述'
  }

  entity app_system_interrupt {
    业务系统中断记录
    ==
    #id bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键'
    interrupt_id varchar(100) DEFAULT NULL COMMENT 'uuid'
    app_id int(11) unsigned NOT NULL COMMENT '业务系统标识'
    start_time datetime NOT NULL COMMENT '业务系统中断开始时间'
    end_time datetime DEFAULT NULL COMMENT '业务系统中断结束时间'
    description varchar(512) DEFAULT NULL COMMENT '描述信息'
  }


  entity ldu_health_weight {
    业务系统组件健康度计算权重表
    ==
    --改名
    #id int(11) NOT NULL AUTO_INCREMENT COMMENT '主键'
    app_id int(11) NOT NULL COMMENT '业务系统id'
    weight varchar(512) NOT NULL COMMENT '权重，以json字符串存储'
  }

  entity mdm_ip {
    ip信息表
    ==
    --租户ID改单位Id,vlanId改int
    #ip_id int(11) AUTO_INCREMENT COMMENT 'ip唯一标识'
    company_id int(11) DEFAULT NULL COMMENT '单位id'
    oss_id int(11) DEFAULT NULL COMMENT '所属管理域Id'
    oss_ip int(11) DEFAULT NULL COMMENT '所属管理域Ip'
    ip varchar(64)  NOT NULL COMMENT 'ip地址'
    mask varchar(32)  DEFAULT NULL COMMENT '子网掩码'
    vlan_id int(11) DEFAULT NULL COMMENT '所属vlanId'
    network_name varchar(64)  DEFAULT NULL COMMENT '网络名称'
    description varchar(512)  DEFAULT NULL COMMENT '描述'
    status int(11) DEFAULT NULL COMMENT '状态'
    +source_uuid varchar(64)  DEFAULT NULL COMMENT '使用者uuid'
    source_name varchar(64)  DEFAULT NULL COMMENT '使用对象名称'
    net_area varchar(64)  DEFAULT NULL COMMENT '所在分区'
    latest_start_time datetime DEFAULT NULL COMMENT '上次占用时间'
    latest_release_time datetime DEFAULT NULLCOMMENT '上次释放时间'
    data_source tinyint(1) DEFAULT '0' COMMENT '数据源 0-自动发现 1-云平台同步'
    host_type varchar(255)  DEFAULT NULL
  }

  entity mdm_ip_his {
    增加ip历史表
    ==
    --租户ID改单位Id
    #his_id int(11) NOT NULL AUTO_INCREMENT
    +ip_id int(11) NOT NULL COMMENT 'Ip表的IP标识'
    company_id int(11) DEFAULT NULL COMMENT '单位id'
    vlan_id int(20) DEFAULT NULL COMMENT '所属网段'
    source_uuid varchar(64)  DEFAULT NULL COMMENT '使用者uuid'
    source_name varchar(64)  DEFAULT NULL COMMENT '使用者名称'
    start_date datetime DEFAULT NULL COMMENT '开始使用时间'
    end_date datetime DEFAULT NULL COMMENT '使用结束时间 - 此记录入库时间'
  }

  entity mdm_vlan {
    vlan信息表
    ==
    --租户ID改单位Id,vlanId改int
    #vlan_id int(11) NOT NULL AUTO_INCREMENT COMMENT '自增id'
    uuid varchar(64)  DEFAULT NULL COMMENT 'vlan的管理域id'
    company_id int(11) DEFAULT NULL COMMENT '租户id'
    vlan_name varchar(64)  DEFAULT NULL COMMENT 'vlan名称'
    vlan_type tinyint(4) DEFAULT NULL COMMENT '1 standard network 2other'
    virtual_datacenter varchar(64)  DEFAULT NULL COMMENT '虚拟中心的名称'
    oss_id int(11) DEFAULT NULL COMMENT '所属管理域 云平台Id'
    net_address varchar(64)  DEFAULT NULL COMMENT '网络地址 如192.168.0.0'
    net_mask varchar(64)  DEFAULT NULL COMMENT 'vlan的子网掩码'
    enabled tinyint(4) DEFAULT '1' COMMENT '1启用 0停用 default 1'
    description varchar(512)  DEFAULT NULL COMMENT '描述'
    data_source tinyint(1) DEFAULT '0'COMMENT '数据源 0-自动发现 1-云平台同步'
  }
```
