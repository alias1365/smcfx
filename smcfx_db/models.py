from django.contrib.auth.models import User
from django.db import models


class expert_key(models.Model):
    name = models.CharField(max_length=200, unique=True)
    user = models.OneToOneField(User, related_name="expert_key_to_user", on_delete=models.CASCADE)
    key = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    deactive_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class trade_account(models.Model):
    user = models.ForeignKey(User, related_name="trade_account_to_user", on_delete=models.CASCADE)
    number = models.BigIntegerField()
    name = models.CharField(max_length=500)
    company = models.CharField(max_length=500)
    balance = models.DecimalField(max_digits=18, decimal_places=2)
    equity = models.DecimalField(max_digits=18, decimal_places=2)
    currency = models.CharField(max_length=200)
    add_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'number', 'company')

    def __str__(self):
        return f"{self.name} - {self.number} - {self.company}"


class trade_position(models.Model):
    account = models.ForeignKey(trade_account, related_name="trade_position_to_trade_account", on_delete=models.CASCADE)
    position_id = models.BigIntegerField()
    symbol = models.CharField(max_length=200)
    type = models.CharField(max_length=30, default="")
    volume = models.DecimalField(max_digits=18, decimal_places=2)
    open_price = models.FloatField(default=0)
    current_price = models.FloatField(default=0)
    sl = models.FloatField(default=0)
    tp = models.FloatField(default=0)
    profit = models.DecimalField(max_digits=18, decimal_places=2)
    commission = models.FloatField(default=0)
    open_time = models.DateTimeField(null=True)
    close_time = models.DateTimeField(null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)
    swap = models.FloatField(default=0)

    class Meta:
        unique_together = ('account', 'position_id')

    def __str__(self):
        return f"{self.account.number} : {self.position_id} - {self.symbol} - {self.open_time}"

    def delete_deals(self):
        trade_deals.objects.filter(position__id=self.id).delete()

    def delete_files(self):
        trade_files.objects.filter(position__id=self.id).delete()

    def deals_have_ticket(self):
        dls = trade_deals.objects.filter(position__id=self.id)
        for itm in dls:
            if itm.ticket == 0:
                return False
        return True

    def deal_count(self):
        return trade_deals.objects.filter(position=self).count()

    def bstext(self):
        try:
            return self.trade_sentiment_to_trade_position.before_text
        except:
            return ""

    def astext(self):
        try:
            return self.trade_sentiment_to_trade_position.after_text
        except:
            return ""

    def tstext(self):
        try:
            return self.trade_sentiment_to_trade_position.trading_text
        except:
            return ""

    def images(self):
        return trade_files.objects.filter(position=self, file_type="img").order_by('file_name')


class trade_deals(models.Model):
    position = models.ForeignKey(trade_position, related_name="trade_deals_to_trade_position", on_delete=models.CASCADE)
    ticket = models.BigIntegerField(default=0)
    type = models.CharField(max_length=200, default="")
    volume = models.DecimalField(max_digits=18, decimal_places=2)
    open_price = models.FloatField(default=0)
    close_price = models.FloatField(default=0)
    profit = models.DecimalField(max_digits=18, decimal_places=2)
    commission = models.DecimalField(max_digits=18, decimal_places=2)
    swap = models.DecimalField(max_digits=18, decimal_places=2)
    open_time = models.DateTimeField(null=True)
    close_time = models.DateTimeField(null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.type} : {self.close_time}"


class trade_files(models.Model):
    position = models.ForeignKey(trade_position, related_name="trade_files_to_trade_position", on_delete=models.CASCADE)
    file_name = models.CharField(max_length=150)
    file_content = models.TextField()
    file_type = models.CharField(max_length=10, default='', blank=True)
    file_tm = models.CharField(max_length=10, default='', blank=True)

    class Meta:
        unique_together = ('position', 'file_name')

    def __str__(self):
        return f"{self.file_name}"


class trader_select_account(models.Model):
    user = models.ForeignKey(User, related_name="trader_select_account_to_user", on_delete=models.CASCADE)
    account = models.ForeignKey(trade_account, related_name="trader_select_account_to_trader_account",
                                on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} -> {self.account.number} : {self.account.name}"


class trade_sentiment(models.Model):
    position = models.OneToOneField(trade_position, related_name="trade_sentiment_to_trade_position",
                                    on_delete=models.CASCADE)
    before_text = models.TextField(default="", blank=True, null=True)
    trading_text = models.TextField(default="", blank=True, null=True)
    after_text = models.TextField(default="", blank=True, null=True)

    def __str__(self):
        return f"{self.position} sentiments."


class trade_rating(models.Model):
    position = models.OneToOneField(trade_position, related_name="trade_rating_to_trade_position",
                                    on_delete=models.CASCADE)
    rate_plan = models.DecimalField(default=None, blank=True, null=True, max_digits=5, decimal_places=1)
    rate_checklist = models.DecimalField(default=None, blank=True, null=True, max_digits=5, decimal_places=1)
    rate_sentiment = models.DecimalField(default=None, blank=True, null=True, max_digits=5, decimal_places=1)
    text_plan = models.TextField(default="", blank=True, null=True)
    text_checklist = models.TextField(default="", blank=True, null=True)
    text_sentiment = models.TextField(default="", blank=True, null=True)


class file_receive_log(models.Model):
    log_date = models.DateTimeField(auto_now_add=True)
    log = models.TextField()
    user = models.ForeignKey(User, related_name="file_receive_log_to_user_ref", on_delete=models.CASCADE)
    log_tag = models.CharField(max_length=20)
    type = models.CharField(max_length=10, default='')

    def __str__(self):
        return self.log


# student models
class student(models.Model):
    user = models.OneToOneField(User, related_name="student_user_ref", on_delete=models.CASCADE)
    mobile = models.CharField(max_length=25)
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=100, null=True, blank=True)
    timezone = models.CharField(max_length=100, null=True, blank=True)
    init_pass = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.user} - {self.mobile}"


# settings models
class expert_setting_risk(models.Model):
    user = models.OneToOneField(User, related_name="user_risk_setting_ref", on_delete=models.CASCADE)
    risk_type = models.SmallIntegerField(default=1)
    risk_percent = models.FloatField(default=1)
    risk_dollar = models.FloatField(default=5)

    def __str__(self):
        return f"setting risk code is : {self.id}"


class expert_setting_monman(models.Model):
    user = models.OneToOneField(User, related_name="user_monman_setting_ref", on_delete=models.CASCADE)
    tp1_exit_vol = models.FloatField(default=0.3)
    tp2_exit_vol = models.FloatField(default=0.3)
    tp3_exit_vol = models.FloatField(default=0.3)
    tp_trail_step = models.FloatField(default=1)

    def __str__(self):
        return f"setting money management code is : {self.id}"


class expert_setting_style(models.Model):
    user = models.OneToOneField(User, related_name="user_style_style_ref", on_delete=models.CASCADE)
    text_color = models.CharField(max_length=50, default="clrYellow")
    London_color = models.CharField(max_length=50, default="clrLime")
    NY_color = models.CharField(max_length=50, default="clrDeepPink")
    Asia_color = models.CharField(max_length=50, default="clrYellow")
    PB_color = models.CharField(max_length=50, default="clrAliceBlue")
    SessionLines = models.SmallIntegerField(default=2)
    SessionHalfLine = models.SmallIntegerField(default=2)
    Position_1_color = models.CharField(max_length=50, default="clrAliceBlue")
    Position_2_color = models.CharField(max_length=50, default="clrYellow")
    Position_3_color = models.CharField(max_length=50, default="clrLime")
    Position_4_color = models.CharField(max_length=50, default="clrPink")
    Position_5_color = models.CharField(max_length=50, default="clrOrange")
    Position_n_color = models.CharField(max_length=50, default="clrRed")
    text_margin = models.SmallIntegerField(default=20)
    text_font_size = models.SmallIntegerField(default=8)
    caption_font_size = models.SmallIntegerField(default=7)
    text_base_width = models.SmallIntegerField(default=28)

    def __str__(self):
        return f"setting style code is : {self.id}"


class expert_setting_session(models.Model):
    user = models.OneToOneField(User, related_name="user_session_setting_ref", on_delete=models.CASCADE)
    session_day_count = models.SmallIntegerField(default=3)
    AsiaStart = models.CharField(max_length=50, default="2:30")
    AsiaEnd = models.CharField(max_length=50, default="9:30")
    LondonStart = models.CharField(max_length=50, default="11:30")
    LondonEnd = models.CharField(max_length=50, default="17:00")
    NyStart = models.CharField(max_length=50, default="17:00")
    NyEnd = models.CharField(max_length=50, default="00:30")

    def __str__(self):
        return f"setting session code is : {self.id}"


class expert_setting_journal(models.Model):
    user = models.OneToOneField(User, related_name="user_journal_setting_ref", on_delete=models.CASCADE)
    M1 = models.BooleanField(default=True, verbose_name="1 Minute")
    M5 = models.BooleanField(default=False, verbose_name="5 Minutes")
    M15 = models.BooleanField(default=True, verbose_name="15 Minutes")
    M30 = models.BooleanField(default=False, verbose_name="30 Minutes")
    H1 = models.BooleanField(default=False, verbose_name="1 Hour")
    H4 = models.BooleanField(default=False, verbose_name="4 Hours")
    D1 = models.BooleanField(default=False, verbose_name="1 Day")
    W1 = models.BooleanField(default=False, verbose_name="1 Week")
    capture_zoom = models.SmallIntegerField(default=1)
    journal_server = models.CharField(max_length=300, default="", blank=True)
    user_token = models.CharField(max_length=300, default="", blank=True)

    def get_tm(self, delimiter=','):
        selected = []
        for tf in ['M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D1', 'W1']:
            if getattr(self, tf):
                selected.append(tf)
        return delimiter.join(selected)

    def __str__(self):
        return f"setting journal code is : {self.id}"


class test_data(models.Model):
    folder = models.CharField(max_length=300)
    token = models.CharField(max_length=300)
    p_stat = models.CharField(max_length=300, default='')


class test_data_file(models.Model):
    mid = models.ForeignKey(test_data, related_name="tst_ref", on_delete=models.CASCADE)
    file_name = models.TextField()
    file_content = models.TextField()
