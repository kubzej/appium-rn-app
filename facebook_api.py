import facebook
import os


class FacebookAPI:
    app_id = os.environ.get("FACEBOOK_APP_ID")
    secret = os.environ.get("FACEBOOK_SECRET")
    token = facebook.GraphAPI().get_app_access_token(app_id, secret, True)
    graph = facebook.GraphAPI(access_token=token)

    def create_test_user(self):
        user = self.graph.request(
            self.app_id + "/accounts/test-users", {}, {}, method="POST"
        )
        return user

    def delete_test_user(self, user):
        self.graph.request(user["id"], {}, None, method="DELETE")
