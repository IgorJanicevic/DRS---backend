from repositories.post_repository import PostRepository



class PostService:

    @staticmethod
    def create_post(data):
        post = PostRepository.create_post(data)
        if post:
            return post,201
        else:
            return {'message': 'Error with create post.'},400
        
    @staticmethod
    def delete_post(post_id):
        try:
            if PostRepository.delete_post(post_id):
                return {'message':'Post successfully deleted.'},200
            else:
                return {'message': 'Post not found'},404
        except:
            return {'message': 'Error with deleting post'},500
        
    @staticmethod
    def get_user_posts(user_id):
        try:
            posts = PostRepository.get_user_posts(user_id)
            if posts:
                return posts,200
            else:
                return {'message': 'Posts not found'},404
        except:
            return {'message','Error with getting self posts'},500
        