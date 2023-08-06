## Cloud Python SDK
该库主要是封装了cloud Iaas的API，进行方便获取与操作IaaS资源

### 安装
使用pip安装
```
pip install cloud-sdk
```
### 实例
```
from cloudsdk.config import ApiConfig
from cloudsdk.models.instance_model import InstanceModel

ApiConfig.config(api_domain='http://api.cloud.com/iaas', api_access_key_id='SKYERWERFDFADUTLNVTI',
                 api_secret_access_key='FADSFDSAFA23FDAFA32FDSAFADS')

print(InstanceModel.get_instance_info_by_instance_id(instance_id='i-lrvoa092'))

```
### 说明
ApiConfig.config

字段 | 说明
--- | ---
api_drivers | cloud sdk驱动，默认为qingcloud
api_domain | IaaS Api服务地址
api_access_key_id | 请求access key
api_secret_access_key | 请求secret key
api_default_zone | 默认可用区zone，默认值为SHA
