#import <Foundation/Foundation.h>

@interface {{ class_name }} : {{ super_name }}

{% for property in properties %}
@property (nonatomic, {{ property.retain_type }}) {{ property.class_name }} {{ property.name }};
{% endfor %}

@end