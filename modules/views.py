from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Module, Registration
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer
from django.core.paginator import Paginator
from django.templatetags.static import static

def module_list(request):
    modules = Module.objects.all()
    categories = Module.objects.values_list('category', flat=True).distinct()
    categories = sorted(set(cat.strip() for cat in categories if cat))
    qualification_types = Module.QUALIFICATION_TYPES
    mode_of_study = Module.MODE_OF_STUDY
    mode_of_delivery = Module.MODE_OF_DELIVERY
    selected_categories = request.GET.getlist('category')
    selected_qualifications = request.GET.getlist('qualification_type')
    selected_mode_of_study = request.GET.getlist('mode_of_study')
    selected_mode_of_delivery = request.GET.getlist('mode_of_delivery')
    search_query = request.GET.get('search', '')

    if search_query:
        modules = modules.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    if selected_categories:
        modules = modules.filter(category__in=selected_categories)
    if selected_qualifications:
        modules = modules.filter(qualification_type__in=selected_qualifications)
    if selected_mode_of_study:
        modules = modules.filter(mode_of_study__in=selected_mode_of_study)
    if selected_mode_of_delivery:
        modules = modules.filter(mode_of_delivery__in=selected_mode_of_delivery)

    # Pagination
    paginator = Paginator(modules, 9)  # Show 9 modules per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        modules_data = [
            {
                'id': module.id,
                'name': f"{module.name} ({module.code})",
                'description': module.description[:60] + ('...' if len(module.description) > 60 else ''),
                'image': module.image.url if module.image else static('img/default_img.jpg'),
                'availability': module.availability,
                'credits': module.credits,
                'detail_url': request.build_absolute_uri(module.get_absolute_url())
            } for module in page_obj.object_list  # Use paginated modules
        ]
        return JsonResponse({'modules': modules_data, 'total_pages': paginator.num_pages, 'current_page': page_obj.number})

    return render(
        request,
        'modules/module_list.html',
        {
            'modules': page_obj,  # Pass the paginator page object
            'categories': categories,
            'selected_categories': selected_categories,
            'qualification_types': qualification_types,
            'selected_qualifications': selected_qualifications,
            'mode_of_study': mode_of_study,
            'selected_mode_of_study': selected_mode_of_study,
            'mode_of_delivery': mode_of_delivery,
            'selected_mode_of_delivery': selected_mode_of_delivery
        }
    )

def module_detail(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    is_registered = Registration.objects.filter(student=request.user, module=module).exists() if request.user.is_authenticated else False
    return render(request, 'modules/module_detail.html', {'module': module, 'is_registered': is_registered})

@login_required
def register(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    if not module.availability:
        messages.error(request, "This module is not available for registration.")
        return redirect('modules:module_detail', module_id=module.id)

    student_course = request.user.groups.first()
    if not student_course:
        messages.error(request, f"No course assigned to user {request.user.username}. Please contact an administrator.")
        return redirect('modules:module_detail', module_id=module.id)
    if student_course not in module.courses.all():
        messages.error(request, f"This module is not available for your course ({student_course.name}). Available courses: {', '.join([course.name for course in module.courses.all()])}.")
        return redirect('modules:module_detail', module_id=module.id)

    registration, created = Registration.objects.get_or_create(student=request.user, module=module)
    messages.success(request, f"Successfully registered for {module.name}.")
    return redirect('modules:module_detail', module_id=module.id)

@login_required
def unregister(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    registration = Registration.objects.filter(student=request.user, module=module).first()
    if registration:
        registration.delete()
        messages.success(request, f"Successfully unregistered from {module.name}.")
    else:
        messages.error(request, f"You are not registered for {module.name}.")
    return redirect('modules:module_detail', module_id=module.id)

@method_decorator(login_required, name='dispatch')
class RegisterModuleAPIView(APIView):
    def post(self, request, module_id):
        try:
            module = Module.objects.get(id=module_id)
        except Module.DoesNotExist:
            return Response({"error": "Module not found."}, status=status.HTTP_404_NOT_FOUND)

        if not module.availability:
            return Response({"error": "This module is not available for registration."}, status=status.HTTP_400_BAD_REQUEST)

        student_course = request.user.groups.first()
        if not student_course:
            return Response({"error": f"No course assigned to user {request.user.username}."}, status=status.HTTP_400_BAD_REQUEST)
        if student_course not in module.courses.all():
            return Response({"error": f"This module is not available for your course ({student_course.name}). Available courses: {', '.join([course.name for course in module.courses.all()])}."}, status=status.HTTP_400_BAD_REQUEST)

        registration, created = Registration.objects.get_or_create(student=request.user, module=module)
        serializer = RegistrationSerializer(registration)
        return Response({
            "message": f"Successfully registered for {module.name}.",
            "registration": serializer.data
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)