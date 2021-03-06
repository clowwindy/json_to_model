// Generated by json_to_model

#import "User.h"

@implementation User  {

}

- (id)initWithJSONDictionary:(NSDictionary *)dictionary {

    self = [super init];
    if (![dictionary isKindOfClass:[NSDictionary class]])
        return nil;

    if (self) {
 
        self.username = (dictionary[@"username"] != [NSNull null]) ? dictionary[@"username"] : nil;
  
        self.age = (dictionary[@"age"] != [NSNull null]) ? [dictionary[@"age"] integerValue] : 0;
  
        self.registered = (dictionary[@"registered"] != [NSNull null]) ? [dictionary[@"registered"] boolValue] : NO;
  
        self.email = (dictionary[@"email"] != [NSNull null]) ? dictionary[@"email"] : nil;
 
    }
    return self;
}

- (id)initWithJSONData:(NSData *)data {
    self = [super init];
    if (self) {
        NSError *error = nil;
        id result = [NSJSONSerialization JSONObjectWithData:data options:NSJSONReadingAllowFragments error:&error];
        if (result) {
            self = [self initWithJSONDictionary:result];
        } else {
            return nil;
        }
    }
    return self;
}

- (NSDictionary *)JSONDictionary {

    NSMutableDictionary *dictionary = [[NSMutableDictionary alloc] init];

 
    dictionary[@"username"] = (self.username != nil) ? self.username : [NSNull null];
  
    dictionary[@"age"] = @(self.age);
  
    dictionary[@"registered"] = @(self.registered);
  
    dictionary[@"email"] = (self.email != nil) ? self.email : [NSNull null];
 
    return dictionary;
}


- (NSData *)JSONData {
    NSError *error = nil;
    NSData *data = [NSJSONSerialization dataWithJSONObject:[self JSONDictionary] options:0 error:&error];
    if (error) {
        @throw error;
    }
    return data;
}


@end