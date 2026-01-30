import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.fixture
def test_user():
    """Создаёт тестового пользователя"""
    return User.objects.create_user(email="test@example.com", password="testpass123")


@pytest.fixture
def test_superuser():
    """Создаёт тестового суперпользователя"""
    return User.objects.create_superuser(
        email="admin@example.com", password="adminpass123"
    )


@pytest.mark.django_db
def test_create_user(test_user):
    """Проверка создания обычного пользователя"""
    assert test_user.email == "test@example.com"
    assert test_user.check_password("testpass123") is True
    assert test_user.is_superuser is False
    assert test_user.is_staff is False


@pytest.mark.django_db
def test_create_superuser(test_superuser):
    """Проверка создания суперпользователя"""
    assert test_superuser.email == "admin@example.com"
    assert test_superuser.is_superuser is True
    assert test_superuser.is_staff is True


@pytest.mark.django_db
def test_user_str(test_user):
    """Проверка строкового представления"""
    assert str(test_user) == "test@example.com"


def test_register_page(client):
    """Страница регистрации открывается"""
    response = client.get("/users/register/")
    assert response.status_code == 200


def test_login_page(client):
    """Страница входа открывается"""
    response = client.get("/users/login/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_profile_requires_auth(client, test_user):
    """Профиль требует авторизации"""
    response = client.get(reverse("profile"))
    assert response.status_code == 302
    assert "/login" in response.url


@pytest.mark.django_db
def test_profile_accessible(client, test_user):
    """Авторизованный пользователь видит профиль"""
    client.login(email="test@example.com", password="testpass123")
    response = client.get(reverse("profile"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_registration_works(client, db):
    """Регистрация создаёт нового пользователя"""
    initial_count = User.objects.count()

    response = client.post(
        reverse("register"),
        {
            "email": "newuser@example.com",
            "password1": "complexpass123",
            "password2": "complexpass123",
        },
    )

    assert response.status_code == 302

    assert User.objects.count() == initial_count + 1
    assert User.objects.filter(email="newuser@example.com").exists()
