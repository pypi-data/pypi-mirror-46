from .utils.gdpaginator import paginate
from .utils.params import Parameters as Params
from .utils.http_request import http
from .utils.routes import Route
from .utils.mapper import mapper_util
from .utils.indexer import Index as i
from .utils.errors import error
from .utils.converter import Converter

class AuthClient:
    def __init__(self, **options):
        self._name = options.get('name')
        self._password = options.get('password')
        self._accountid = options.get('accountid')
        self._userid = options.get('userid')
        self._encodedpass = options.get('encodedpass')
        self._dict = {
            'name': options.get('name'),
            'id': options.get('userid'),
            'account_id': options.get('accountid')
        }
        from .client import client
        self._as_user = client().get_user(str(options.get('accountid')))

    def __str__(self):
        ret = f"[gd.AuthClient]\n[Name:{self.name}]\n[Password:{self.password}]\n[AccountID:{self.account_id}]\n[UserID:{self.id}]\n<'{self.encodedpass}'>"
        return ret

    @property
    def name(self):
        return self._name
    @property
    def password(self):
        return self._password
    @property
    def encodedpass(self):
        return self._encodedpass
    @property
    def account_id(self):
        return self._accountid
    @property
    def id(self):
        return self._userid

    def as_user(self):
        return self._as_user
    
    def get_comments(self, **kwargs):
        from .classconverter import class_converter
        _paginate = kwargs.get('paginate') if kwargs.get('paginate') is not None else False
        per_page = Converter.write_per_page(**kwargs)
        route = Route.GET_COMMENTS 
        parameters = Params().create_new().put_definer('accountid', str(self.account_id)).put_page(0).put_total(0).finish()
        resp = http.SendHTTPRequest(route, parameters)
        to_map = resp.split('#')
        comments = []
        if (len(to_map[0])==0):
            raise error.NothingFound('comments')
        else:
            to_map = to_map[0].replace('-', '+').split('|') #I don't know why but this one is actually intended
            for element in to_map:
                mapped = mapper_util.map(element.split('~'))
                comments.append(class_converter.CommentConvert(mapped, self._dict))
            if not _paginate:
                return comments
            else:
                paginator = paginate(comments, per_page=per_page)
                return paginator
    

    def get_friends(self, **kwargs):
        from .classconverter import class_converter
        _paginate = kwargs.get('paginate') if kwargs.get('paginate') is not None else False
        id_mode = kwargs.get('id_mode') if kwargs.get('id_mode') is not None else False
        per_page = Converter.write_per_page(**kwargs)
        route = Route.GET_FRIENDS
        parameters = Params().create_new().put_definer('accountid', str(self.account_id)).put_password(self.encodedpass).put_type(0).finish()
        ids, objects = [], []
        resp = http.SendHTTPRequest(route, parameters)
        if resp == '-1':
            raise error.MissingAccess()
        if resp == '-2':
            raise error.NothingFound('friends')
        else:
            to_map = resp.split('|')
        for element in to_map:
            ids.append(int((mapper_util.map(element.split(':'))[i.USER_ACCOUNT_ID]))) #you say '()'? lol
        if id_mode:
            return ids
        else:
            for element in to_map:
                temp = (mapper_util.map(element.split(':')))
                temp_accid = int(temp[i.USER_ACCOUNT_ID])
                temp_id = int(temp[i.USER_PLAYER_ID])
                temp_name = str(temp[i.USER_NAME])
                some_dict = {
                    'name': temp_name,
                    'id': temp_id,
                    'account_id': temp_accid
                }
                converted = class_converter.AbstractUserConvert(some_dict)
                objects.append(converted)
            if not _paginate:
                return objects
            else:
                paginator = paginate(objects, per_page=per_page)
                return paginator
    
    def post_comment(self, content: str = None):
        if content is None:
            raise error.MissingArguments()
        else:
            route = Route.UPLOAD_ACC_COMMENT
            to_gen = [self.name, 0, 0, 1]
            parameters = Params().create_new().put_definer('accountid', str(self.account_id)).put_username(self.name).put_password(self.encodedpass).put_comment(content, to_gen).comment_for('client').finish()
            resp = http.SendHTTPRequest(route, parameters)
            if resp == '-1':
                raise error.MissingAccess()
            return self.get_comments()[0]
    
    def get_messages(self, sent_or_inbox: str = None):
        from .classconverter import class_converter
        if sent_or_inbox is None:
            inbox = 0
        if (sent_or_inbox == 'sent'):
            inbox = 1
        else:
            print(type(sent_or_inbox))
            raise error.InvalidArgument()
        route = Route.GET_PRIVATE_MESSAGES
        parameters = Params().create_new().put_definer('accountid', str(self.account_id)).put_password(self.encodedpass).put_page(0).put_total(0).get_sent(inbox).finish()
        resp = http.SendHTTPRequest(route, parameters)
        if resp == '-1':
            raise error.MissingAccess()
        if resp == '-2':
            raise error.NothingFound('messages')
        else:
            to_map = resp.split('|')
        for element in to_map:
            temp = element.split(':')
            #I need to think how it'll look like