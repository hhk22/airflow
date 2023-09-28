
def get_sftp():
    print('start sftp job')

def regist(name, sex, *args):
    print(f"name:{name}, sex:{sex}, options: {args}")

def regist2(name, sex, *args, **kwargs):
    print(f'name: {name}, sex: {sex}, options: {args}')
    email = kwargs.get('email')
    phone = kwargs.get('phone')
    if email:
        print(f'email: {email}')
    if phone:
        print(f'phone: {phone}')
        