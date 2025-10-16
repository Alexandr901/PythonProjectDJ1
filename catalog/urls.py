from django.urls import path

from .views import (CategoriesListView, CategoryProductsView, ContactsView,
                    HomeView, ProductCreateView, ProductDeleteView,
                    ProductDetailView, ProductUnpublishView, ProductUpdateView)

app_name = "catalog"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("product/create/", ProductCreateView.as_view(), name="product_create"),
    path("product/<int:pk>/edit/", ProductUpdateView.as_view(), name="product_update"),
    path(
        "product/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"
    ),
    path(
        "product/<int:pk>/unpublish/",
        ProductUnpublishView.as_view(),
        name="product_unpublish",
    ),
    # Новые маршруты для категорий
    path("categories/", CategoriesListView.as_view(), name="categories_list"),
    path(
        "category/<slug:category_slug>/",
        CategoryProductsView.as_view(),
        name="category_products",
    ),
]
