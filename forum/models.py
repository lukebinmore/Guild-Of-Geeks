from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from dateutil.relativedelta import relativedelta
from datetime import date

# Tuples for choice input.
THEMES = (("Light", "Light"), ("Dark", "Dark"))
STATE = ((0, "Draft"), (1, "Post"))
CONTACT_REASON = (
    (0, "Compliment"),
    (1, "Complaint"),
    (2, "Issue"),
    (3, "Request"),
)


# It creates a model for the contact requests.
class ContactRequests(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    reason = models.IntegerField(choices=CONTACT_REASON, default=0)
    title = models.CharField(max_length=50)
    content = models.TextField()
    resolved = models.BooleanField(default=False)

    def __str__(self):
        """
        Returns the request title when printing the object.
        """
        return self.title


# It creates a model for the user's profile.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    dob = models.DateField(max_length=8)
    email = models.EmailField(blank=True)
    number = models.CharField(max_length=11, blank=True)
    picture = CloudinaryField(
        "image", default="static/images/profile-placeholder"
    )
    theme = models.CharField(max_length=25, choices=THEMES, default="Light")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    followed_posts = models.ManyToManyField(
        "Post", related_name="followed_posts", blank=True
    )
    followed_categories = models.ManyToManyField(
        "Category", related_name="followed_categories", blank=True
    )

    def __str__(self):
        """
        Returns the username when printing object.
        """
        return self.user.username

    def get_age(self):
        """
        It returns the age of the person.
        """
        return relativedelta(date.today(), self.dob).years


# It creates a model for the post category.
class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)

    # Defines the ordering of the objects.
    class Meta:
        ordering = ["title"]

    def __str__(self):
        """
        Returns the category title when printing the object.
        """
        return self.title


# It creates a model for the post tags.
class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)

    # Defines the ordering of the objects.
    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


# It creates a model for the posts.
class Post(models.Model):
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    status = models.IntegerField(choices=STATE, default=0)
    likes = models.ManyToManyField(User, related_name="blog_likes", blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="blog_categories"
    )
    tags = models.ManyToManyField(Tag, related_name="blog_tags")

    # Defines the ordering of the objects.
    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        """
        Returns the post title when printing the object.
        """
        return self.title

    def likes_count(self):
        """
        It returns the number of likes for a given post
        :return: The number of likes for a particular post.
        """
        return self.likes.count()

    def comments_count(self):
        """
        It returns the number of comments associated with a post
        :return: The number of comments associated with the post.
        """
        return self.post_comments.count()


# It creates a model for the comments.
class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comments"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comments"
    )
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    reply_to = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True
    )
    likes = models.ManyToManyField(
        User, related_name="comment_likes", blank=True
    )

    # Defines the ordering of the objects.
    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        """
        Returns a formtted string when printing the object.
        """
        return f"{self.content} - (Posted By: {self.author})"
