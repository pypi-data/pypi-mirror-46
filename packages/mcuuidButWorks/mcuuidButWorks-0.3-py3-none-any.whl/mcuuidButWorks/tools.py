def is_valid_minecraft_username(username):
    """https://help.mojang.com/customer/portal/articles/928638-minecraft-usernames"""
    allowed_chars = 'abcdefghijklmnopqrstuvwxyz1234567890_'
    allowed_len = [3, 16]

    username = username.lower()

    if len(username) < allowed_len[0] or len(username) > allowed_len[1]:
        return False

    for char in username:
        if char not in allowed_chars:
            return False

    return True

def is_valid_mojang_uuid(uuid):
    """https://minecraft-de.gamepedia.com/UUID"""
    allowed_chars = '0123456789abcdef'
    allowed_len = 32

    uuid = uuid.lower()

    if len(uuid) != 32:
        return False

    for char in uuid:
        if char not in allowed_chars:
            return False

    return True
