from rest_framework.routers import DefaultRouter

from .views import ClaseViewSet, CursoViewSet, InscripcionViewSet, PagoViewSet

router = DefaultRouter()
router.register('cursos', CursoViewSet, basename='curso')
router.register('clases', ClaseViewSet, basename='clase')
router.register('inscripciones', InscripcionViewSet, basename='inscripcion')
router.register('pagos', PagoViewSet, basename='pago')

urlpatterns = router.urls
