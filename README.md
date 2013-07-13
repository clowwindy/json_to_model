JSON to model
=============

Convert JSON api to Objective-C model (other languages as well in the future)

Got tired of writing models and JSON parsers? Then generate them automatically!

Please consider contributing code. Please send me bug reports and issues.

usage
-----

Suppose you have a json file `~/api/comment.json`:

```json
{
    "__class__": "HMRLatestComment",
    "hottest": [{
        "__class__": "HMRComment",
        "comment_id": 0,
        "author": "",
        "own": false
    }],
    "latest": [{
        "__class__": "HMRComment",
        "comment_id": 0,
        "author": "",
        "own": false
    }]
}
```

Run:

    pip install json_to_model
    json_to_model path/to/json -i ~/api -o ~/models

You'll get:

    ~/models/HMRLatestComment.h
    ~/models/HMRLatestComment.m
    ~/models/HMRComment.h
    ~/models/HMRComment.m

Both models provide conversion methods from/to JSON data.

NSNull are automatically handled. Children of array are also automatically converted.

~/models/HMRLatestComment.h:

```objc
#import <Foundation/Foundation.h>
#import "HMRComment.h"

@interface HMRLatestComment : NSObject

- (id)initWithJSONData:(NSData *)data;
- (id)initWithJSONDictionary:(NSDictionary *)dictionary;
- (NSDictionary *)JSONDictionary;
- (NSData *)JSONData;

@property (nonatomic, strong) NSArray * hottest;
@property (nonatomic, strong) NSArray * latest;

@end
```
   
~/models/HMRComment.h:

```objc
#import <Foundation/Foundation.h>

@interface HMRComment : NSObject

- (id)initWithJSONData:(NSData *)data;
- (id)initWithJSONDictionary:(NSDictionary *)dictionary;
- (NSDictionary *)JSONDictionary;
- (NSData *)JSONData;

@property (nonatomic, assign) BOOL own;
@property (nonatomic, copy) NSString * author;
@property (nonatomic, assign) NSInteger commentId;

@end
```

And a peek at the [HMRLatestComment initWithJSONDictionary]:

```objc
- (id)initWithJSONDictionary:(NSDictionary *)dictionary {

    self = [super init];

    if (self) {
        self.hottest = [[NSMutableArray alloc] initWithCapacity:16];
        for (NSDictionary *_ in dictionary[@"hottest"]) {
                [((NSMutableArray *)self.hottest) addObject:[[HMRComment alloc] initWithJSONDictionary:_]];
        }
        self.latest = [[NSMutableArray alloc] initWithCapacity:16];
        for (NSDictionary *_ in dictionary[@"latest"]) {
                [((NSMutableArray *)self.latest) addObject:[[HMRComment alloc] initWithJSONDictionary:_]];
        }
    }
    return self;
}
```

[HMRComment initWithJSONDictionary]:

```objc
- (id)initWithJSONDictionary:(NSDictionary *)dictionary {

    self = [super init];

    if (self) {
        self.own = [dictionary[@"own"] boolValue];
        self.author = (dictionary[@"author"] != [NSNull null]) ? dictionary[@"author"] : nil;
        self.commentId = [dictionary[@"comment_id"] integerValue];
    }
    return self;
}
```
