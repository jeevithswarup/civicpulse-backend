from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils.timezone import now
from django.core.cache import cache
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from datetime import timedelta
from complaints.models import Complaint
from users.models import User


class PlatformStatsView(APIView):
    """Admin: high-level platform numbers. Cached 60s."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        cached = cache.get("platform_stats")
        if cached:
            return Response(cached)

        data = {
            'total_complaints': Complaint.objects.count(),
            'resolved':         Complaint.objects.filter(status='resolved').count(),
            'pending':          Complaint.objects.filter(status='pending').count(),
            'in_progress':      Complaint.objects.filter(status='in_progress').count(),
            'active_today':     Complaint.objects.filter(created_at__date=now().date()).count(),
            'total_citizens':   User.objects.filter(role='citizen').count(),
            'active_officers':  User.objects.filter(role='officer').count(),
            'total_workers':    User.objects.filter(role='worker').count(),
        }
        cache.set("platform_stats", data, timeout=60)
        return Response(data)


class DailyTrendView(APIView):
    """Admin/Officer: complaints per day for last 30 days. Cached 5 min."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cached = cache.get("daily_trend")
        if cached:
            return Response(cached)

        since = now().date() - timedelta(days=29)

        filed = (
            Complaint.objects
            .filter(created_at__date__gte=since)
            .annotate(day=TruncDate('created_at'))
            .values('day')
            .annotate(complaints=Count('id'))
            .order_by('day')
        )
        resolved = (
            Complaint.objects
            .filter(status='resolved', updated_at__date__gte=since)
            .annotate(day=TruncDate('updated_at'))
            .values('day')
            .annotate(resolved=Count('id'))
            .order_by('day')
        )

        data = {}
        for i in range(30):
            d = since + timedelta(days=i)
            data[d.isoformat()] = {'day': d.strftime('%b %d'), 'complaints': 0, 'resolved': 0}

        for row in filed:
            key = row['day'].isoformat()
            if key in data:
                data[key]['complaints'] = row['complaints']

        for row in resolved:
            key = row['day'].isoformat()
            if key in data:
                data[key]['resolved'] = row['resolved']

        result = list(data.values())
        cache.set("daily_trend", result, timeout=300)
        return Response(result)


class CategoryDistributionView(APIView):
    """Admin/Officer: complaint count by category. Cached 5 min."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cached = cache.get("category_distribution")
        if cached:
            return Response(cached)

        rows = (
            Complaint.objects
            .values('category')
            .annotate(value=Count('id'))
            .order_by('-value')
        )
        result = [
            {'key': r['category'], 'name': r['category'].capitalize(), 'value': r['value']}
            for r in rows
        ]
        cache.set("category_distribution", result, timeout=300)
        return Response(result)


class StatusDistributionView(APIView):
    """Admin/Officer: complaint count by status. Cached 2 min."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cached = cache.get("status_distribution")
        if cached:
            return Response(cached)

        rows = (
            Complaint.objects
            .values('status')
            .annotate(value=Count('id'))
            .order_by('-value')
        )
        STATUS_LABELS = {
            'pending': 'Pending', 'assigned': 'Assigned',
            'in_progress': 'In Progress', 'resolved': 'Resolved', 'closed': 'Closed',
        }
        result = [
            {'key': r['status'], 'name': STATUS_LABELS.get(r['status'], r['status']), 'value': r['value']}
            for r in rows
        ]
        cache.set("status_distribution", result, timeout=120)
        return Response(result)


class ResolutionTrendView(APIView):
    """Admin/Officer: daily resolution rate % for last 7 days. Cached 5 min."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cached = cache.get("resolution_trend")
        if cached:
            return Response(cached)

        since = now().date() - timedelta(days=6)
        result = []
        for i in range(7):
            d = since + timedelta(days=i)
            total = Complaint.objects.filter(created_at__date=d).count()
            resolved = Complaint.objects.filter(status='resolved', updated_at__date=d).count()
            rate = round((resolved / total * 100), 1) if total > 0 else 0
            result.append({'day': d.strftime('%b %d'), 'resolutionRate': rate})

        cache.set("resolution_trend", result, timeout=300)
        return Response(result)
