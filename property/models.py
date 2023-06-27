import uuid
from django.db import models
from django.contrib.auth import get_user_model

from services.constant import FOOD_INCLUDED_DETAILS, PARKING, PG_AMENITIES, PG_AVAILABLE_FOR, PG_OTHER_DETAILS, PREFERRED_TENANTS, PROPERTY_AD_TYPE, PROPERTY_CITIES, PROPERTY_EXTRA_FEATURES

from multiselectfield import MultiSelectField

User = get_user_model()


class Property(models.Model):
    # owner details
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    property_ad_type = models.CharField(max_length=20, choices=PROPERTY_AD_TYPE)
    # room details
    single_room = models.BooleanField(default=False)
    double_room = models.BooleanField(default=False)
    triple_room = models.BooleanField(default=False)
    four_room = models.BooleanField(default=False)
    single_room_expected_rent = models.IntegerField(null=True, blank=True)
    single_room_deposit_rent = models.IntegerField(null=True, blank=True)
    single_room_extra_features = MultiSelectField(choices=PROPERTY_EXTRA_FEATURES, null=True, blank=True)
    double_room_expected_rent = models.IntegerField(null=True, blank=True)
    double_room_deposit_rent = models.IntegerField(null=True, blank=True)
    double_room_extra_features = MultiSelectField(choices=PROPERTY_EXTRA_FEATURES, null=True, blank=True)
    triple_room_expected_rent = models.IntegerField(null=True, blank=True)
    triple_room_deposit_rent = models.IntegerField(null=True, blank=True)
    triple_room_extra_features = MultiSelectField(choices=PROPERTY_EXTRA_FEATURES, null=True, blank=True)
    four_room_expected_rent = models.IntegerField(null=True, blank=True)
    four_room_deposit_rent = models.IntegerField(null=True, blank=True)
    four_room_extra_features = MultiSelectField(choices=PROPERTY_EXTRA_FEATURES, null=True, blank=True)
    # location details
    city = models.CharField(max_length=100, choices=PROPERTY_CITIES)
    locality = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100, verbose_name="Landmark/Street")
    pg_name = models.CharField(max_length=100, verbose_name="PG/Hostel Name")
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    # pg/hostel details
    pg_available_for = models.CharField(max_length=100, verbose_name="PG/Hostel Available For", choices=PG_AVAILABLE_FOR)
    preferred_tenants = models.CharField(max_length=100, choices=PREFERRED_TENANTS)
    available_date = models.DateField(null=True, blank=True)
    food_included = models.BooleanField(null=True, blank=True)
    food_included_details = MultiSelectField(choices=FOOD_INCLUDED_DETAILS, null=True, blank=True)
    gate_closing_time = models.TimeField(null=True, blank=True)
    pg_other_details = MultiSelectField(choices=PG_OTHER_DETAILS, null=True, blank=True)
    pg_other_rules = models.TextField(null=True, blank=True, default="")
    # pg services
    laundry = models.BooleanField(null=True, blank=True)
    worden = models.BooleanField(null=True, blank=True)
    room_cleaning = models.BooleanField(null=True, blank=True)
    parking = models.CharField(max_length=100, null=True, blank=True, choices=PARKING)
    pg_amenities = MultiSelectField(choices=PG_AMENITIES, null=True, blank=True)
    property_description = models.TextField(null=True, blank=True, default="")

    image_1 = models.ImageField(upload_to='property_images', null=True, blank=True)
    image_2 = models.ImageField(upload_to='property_images', null=True, blank=True)
    image_3 = models.ImageField(upload_to='property_images', null=True, blank=True)
    image_4 = models.ImageField(upload_to='property_images', null=True, blank=True)
    image_5 = models.ImageField(upload_to='property_images', null=True, blank=True)
    image_6 = models.ImageField(upload_to='property_images', null=True, blank=True)
    image_7 = models.ImageField(upload_to='property_images', null=True, blank=True)
    image_8 = models.ImageField(upload_to='property_images', null=True, blank=True)
    image_9 = models.ImageField(upload_to='property_images', null=True, blank=True)

    near_by_railway_station = models.CharField(max_length=100, null=True, blank=True)
    near_by_bus_stand = models.CharField(max_length=100, null=True, blank=True)
    near_by_market = models.CharField(max_length=100, null=True, blank=True)
    near_by_hospital = models.CharField(max_length=100, null=True, blank=True)
    near_by_bank = models.CharField(max_length=100, null=True, blank=True)
    near_by_airport = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    @property
    def min_amount(self):
        response = {}
        room = []
        if self.single_room_expected_rent != None and self.single_room_expected_rent != 0:
            room.append(self.single_room_expected_rent)
        if self.double_room_expected_rent != None and self.double_room_expected_rent != 0:
            room.append(self.double_room_expected_rent)
        if self.triple_room_expected_rent != None and self.triple_room_expected_rent != 0:
            room.append(self.triple_room_expected_rent)
        if self.four_room_expected_rent != None and self.four_room_expected_rent != 0:
            room.append(self.four_room_expected_rent)
        if len(room) > 0:
            amount = min(room)
        if amount == self.single_room_expected_rent:
            response['room_type'] = 'Single'
        elif amount == self.double_room_expected_rent:
            response['room_type'] = 'Double'
        elif amount == self.triple_room_expected_rent:
            response['room_type'] = 'Triple'
        elif amount == self.four_room_expected_rent:
            response['room_type'] = 'Four'
        response['amount'] = amount
        return response

    @property
    def max_amount(self):
        amount = 0
        if self.single_room_expected_rent == None and self.double_room_expected_rent is not None and self.triple_room_expected_rent is not None and self.four_room_expected_rent is not None:
            amount = max(self.double_room_expected_rent, self.triple_room_expected_rent, self.four_room_expected_rent)
        elif self.single_room_expected_rent is not None and self.double_room_expected_rent == None and self.triple_room_expected_rent is not None and self.four_room_expected_rent is not None:
            amount = max(self.single_room_expected_rent, self.triple_room_expected_rent, self.four_room_expected_rent)
        elif self.single_room_expected_rent is not None and self.double_room_expected_rent is not None and self.triple_room_expected_rent == None and self.four_room_expected_rent is not None:
            amount = max(self.single_room_expected_rent, self.double_room_expected_rent, self.four_room_expected_rent)
        elif self.single_room_expected_rent is not None and self.double_room_expected_rent is not None and self.triple_room_expected_rent is not None and self.four_room_expected_rent == None:
            amount = max(self.single_room_expected_rent, self.double_room_expected_rent, self.triple_room_expected_rent)
        elif self.single_room_expected_rent is not None and self.double_room_expected_rent is not None and self.triple_room_expected_rent is not None and self.four_room_expected_rent is not None:
            amount = max(self.single_room_expected_rent, self.double_room_expected_rent, self.triple_room_expected_rent, self.four_room_expected_rent)
        elif self.single_room_expected_rent is not None and self.double_room_expected_rent is not None and self.triple_room_expected_rent is not None and self.four_room_expected_rent is None:
            amount = max(self.single_room_expected_rent, self.double_room_expected_rent, self.triple_room_expected_rent)
        elif self.single_room_expected_rent is not None and self.double_room_expected_rent is not None and self.triple_room_expected_rent is None and self.four_room_expected_rent is None:
            amount = max(self.single_room_expected_rent, self.double_room_expected_rent)
        elif self.single_room_expected_rent is not None and self.double_room_expected_rent is None and self.triple_room_expected_rent is None and self.four_room_expected_rent is None:
            amount = self.single_room_expected_rent
        elif self.single_room_expected_rent is None and self.double_room_expected_rent is not None and self.triple_room_expected_rent is None and self.four_room_expected_rent is None:
            amount = self.double_room_expected_rent
        elif self.single_room_expected_rent is None and self.double_room_expected_rent is None and self.triple_room_expected_rent is not None and self.four_room_expected_rent is None:
            amount = self.triple_room_expected_rent
        elif self.single_room_expected_rent is None and self.double_room_expected_rent is None and self.triple_room_expected_rent is None and self.four_room_expected_rent is not None:
            amount = self.four_room_expected_rent
        else:
            return None
        return amount

    @property
    def thumbnail(self):
        if self.image_1:
            return self.image_1.url
        elif self.image_2:
            return self.image_2.url
        elif self.image_3:
            return self.image_3.url
        elif self.image_4:
            return self.image_4.url
        elif self.image_5:
            return self.image_5.url
        elif self.image_6:
            return self.image_6.url
        elif self.image_7:
            return self.image_7.url
        elif self.image_8:
            return self.image_8.url
        elif self.image_9:
            return self.image_9.url
        return None

    def __str__(self):
        return self.pg_name

    class Meta:
        verbose_name_plural = "Properties"

