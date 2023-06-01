from django.db import models

class Addresses(models.Model):
    created = models.DateTimeField(auto_now_add=True)



    user_id = models.CharField(max_length=10)
    user_pwd = models.CharField(max_length=13)
    user_list = models.JSONField()
    user_num = models.IntegerField()
    friend_list = models.JSONField()
    friend_num = models.IntegerField()
    history_friend = models.JSONField()
    history_num = models.IntegerField()
    history_friend2 = models.JSONField()
    history_num2 = models.IntegerField()
    history_friend3 = models.CharField(max_length=10)
    history_num3 = models.CharField(max_length=10)
    history_RT = models.CharField(max_length=10)
    history_RT_num = models.CharField(max_length=10)
    checkList = models.JSONField()
    period = models.IntegerField()




    history_RT = "엄마"
    history_RT_num = "시작 날짜 2012년 1월 30일"
    history_friend3 = "제니"
    history_num3 = "스페인"
    history_friend2 = ["여행1", "여행2", "여행3", "스페인", "영국"]
    history_num2 = 5
    history_friend = ["지수", "아빠", "형", "장승우", "엄마", "제니"]
    history_num = 6
    friend_list = ["moonsun2", "moonsun3"]
    friend_num = 2
    user_list = [["moonsun", "1234", "최준혁"], ["moonsun2", "1234", "장승우"],["moonsun3", "1234", "권일"],["moonsun4", "1234", "정성원"]]
    user_num = 4


















    class Meta:
        ordering = ['created']
