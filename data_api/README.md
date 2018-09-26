# Data_API documentation

## Structure

``` python
\data_api:
	admin.py
		register models in admin.app
	apps.py
		register data_api as an app
	forms.py
		serves as a form validater and filter
	models.py
		数据的定义和关系定义
	serializers.py
		generate a serialized object out of model definition
	urls.py
		in-app routing configuration
	views.py
		display settings that generate views of website

```

## Models


![Models Relationships][./Data_api.png]
[./Data_api.png]: ./Data_api.png "Data relationship"


## TODO

### 重构
分拆和人相关的Patient Practitioner Practitioner Membership和 Hospital
加入用户的组织
	
