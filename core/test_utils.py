import datetime

from rest_framework.test import APIClient, APITestCase

from category.models import Category
from comment.models import Comment
from favourites.models import Favourite
from item.models import Item
from offer.models import Offer
from post.models import Post
from tag.models import Tag
from user.models import User


class IAPITestCase(APITestCase):
    counter = 1

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.test_user = User.objects.create_user(email='foo@foo.foo', first_name='Foo', last_name='Bar', nickname='Foo',
                                                 password='1234567890')
        cls.test_user2 = User.objects.create_user(email='foo2@bar.foo', first_name='Foo2', last_name='Foo2',
                                                  nickname='Foo2', password='1234567890')

        cls.test_admin = User.objects.create_superuser(email='admin@admin.admin', first_name='Admin',
                                                       last_name='Admin', nickname='Admin',
                                                       password='1234567890')

        cls.test_category1 = Category.objects.create(name='Wszystko', parent=None, img=None)
        cls.test_category2 = Category.objects.create(name='Pierwsza', parent=cls.test_category1, img=None)
        cls.test_category3 = Category.objects.create(name='Pierwsza', parent=cls.test_category2, img=None)

        cls.test_item = Item.objects.create(name='Item1', category=cls.test_category2, color=Item.Colors.RED,
                                            ready_in=Item.Days.MONTH)
        cls.test_item2 = Item.objects.create(name='Item2', category=cls.test_category2, color=Item.Colors.GOLD,
                                             ready_in=Item.Days.MONTH)
        cls.test_item3 = Item.objects.create(name='Item3', category=cls.test_category3, color=Item.Colors.BLUE,
                                             ready_in=Item.Days.MONTH)
        cls.test_item4 = Item.objects.create(name='Item4', category=cls.test_category3, color=Item.Colors.BLACK,
                                             ready_in=Item.Days.MONTH)

        cls.test_tag = Tag.objects.create(word='Tag1')
        cls.test_tag2 = Tag.objects.create(word='Tag2')
        cls.test_tag3 = Tag.objects.create(word='Tag3')

        cls.test_offer = Offer.objects.create(owner=cls.test_user, item=cls.test_item, price=125, description='Opis1',
                                              gender=Offer.GenderType.WOMAN, date=datetime.datetime.now(),
                                              shipping_abroad=Offer.ShippingAbroad.TRUE)
        cls.test_offer.tag.set([cls.test_tag, cls.test_tag2, cls.test_tag3])

        cls.test_offer2 = Offer.objects.create(owner=cls.test_user, item=cls.test_item2, price=75, description='Opis2',
                                               gender=Offer.GenderType.MAN, date=datetime.datetime.now(),
                                               shipping_abroad=Offer.ShippingAbroad.FALSE)
        cls.test_offer2.tag.set([cls.test_tag2])

        cls.test_offer3 = Offer.objects.create(owner=cls.test_user2, item=cls.test_item3, price=105,
                                               description='Opis3',
                                               gender=Offer.GenderType.KID, date=datetime.datetime.now(),
                                               shipping_abroad=Offer.ShippingAbroad.FALSE)
        cls.test_offer3.tag.set([cls.test_tag3])

        cls.test_like = Favourite.objects.create(user=cls.test_user2, offer=cls.test_offer)
        cls.test_like2 = Favourite.objects.create(user=cls.test_user, offer=cls.test_offer2)
        cls.test_like3 = Favourite.objects.create(user=cls.test_user, offer=cls.test_offer3)

        cls.test_post = Post.objects.create(title='Post1', owner=cls.test_user2, content='Treść postu 1',
                                            date_posted=datetime.datetime.now())

        cls.test_post2 = Post.objects.create(title='Post2', owner=cls.test_user, content='Treść postu 2',
                                             date_posted=datetime.datetime.now())

        cls.test_post3 = Post.objects.create(title='Post3', owner=cls.test_user2, content='Treść postu 3',
                                             date_posted=datetime.datetime.now())

        cls.test_offer_comment = Comment.objects.create(owner=cls.test_user, offer=cls.test_offer,
                                                        content='Kolentarz 1')
        cls.test_offer_comment2 = Comment.objects.create(owner=cls.test_user2, offer=cls.test_offer2,
                                                         content='Kolentarz 2')
        cls.test_offer_comment3 = Comment.objects.create(owner=cls.test_user, offer=cls.test_offer3,
                                                         content='Kolentarz 3')

    def setUp(self):
        print('\n  -------------- Test nr {}-------------- \n '.format(self.counter))

    @classmethod
    def tearDown(cls):
        cls.counter += 1
