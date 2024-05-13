from simplegram import SG

from simplegram.controllers.auth import *
from simplegram.controllers.post import *

SG.route('/')(index)
SG.route('/addpost', methods=['GET', 'POST'])(add_post)
SG.route('/editpost/<post_id>', methods=['GET', 'POST'])(edit_post)
SG.route('/delpost/<post_id>')(del_post)
SG.route('/api/comments/<post_id>')(api_comments)
SG.route('/addcomment/<post_id>', methods=['GET', 'POST'])(add_comment)
SG.route('/login')(login)
SG.route('/login', methods=['POST'])(login_post)
SG.route('/logout')(logout)
SG.route('/register')(register)
SG.route('/register', methods=['POST'])(register_post)
SG.route('/mypost')(my_post)
# Ini Tambahan Kode Saya
SG.route('/mybookmark')(my_bookmark)
SG.route('/addbookmark/<post_id>')(add_bookmark)
SG.route('/delbookmark/<post_id>')(del_bookmark)
SG.route('/delsbookmark/<post_id>')(dels_bookmark)
SG.route('/mailbox')(mailbox)
SG.route('/sendmail', methods=['GET', 'POST'])(sendmail)
SG.route('/delete_message/<message_id>')(delete_message)
SG.route('/like/<post_id>')(like_post)
SG.route('/unlike/<post_id>')(unlike_post)
SG.route('/showlikes/<post_id>')(show_likes)
SG.route('/myprofile', methods=['GET', 'POST'])(my_profile)
SG.route('/profil/<username>')(view_profil)