from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import User, StudentProfile, Notification
from subjects.models import Subject, Chapter
from study_materials.models import StudyMaterial
from questions.models import Question, AnswerOption
from assessments.models import Exam, ExamAttempt
from progress.models import ChapterProgress, QuestionAttempt
from gamification.models import Badge, UserBadge, Point, Leaderboard
from tags.models import Tag
from likes.models import LikedItem


class Command(BaseCommand):
    help = "Creates default user groups and assigns permissions"

    def handle(self, *args, **kwargs):
        # Create groups
        admin_group, _ = Group.objects.get_or_create(name="Administrators")
        content_manager_group, _ = Group.objects.get_or_create(name="Content Managers")
        academic_staff_group, _ = Group.objects.get_or_create(name="Academic Staff")
        support_staff_group, _ = Group.objects.get_or_create(
            name="Student Support Staff"
        )

        # Get content types for all models
        study_material_ct = ContentType.objects.get_for_model(StudyMaterial)
        subject_ct = ContentType.objects.get_for_model(Subject)
        chapter_ct = ContentType.objects.get_for_model(Chapter)
        question_ct = ContentType.objects.get_for_model(Question)
        answer_ct = ContentType.objects.get_for_model(AnswerOption)
        exam_ct = ContentType.objects.get_for_model(Exam)
        exam_attempt_ct = ContentType.objects.get_for_model(ExamAttempt)
        badge_ct = ContentType.objects.get_for_model(Badge)
        user_badge_ct = ContentType.objects.get_for_model(UserBadge)
        point_ct = ContentType.objects.get_for_model(Point)
        student_profile_ct = ContentType.objects.get_for_model(StudentProfile)
        notification_ct = ContentType.objects.get_for_model(Notification)
        progress_ct = ContentType.objects.get_for_model(ChapterProgress)
        question_attempt_ct = ContentType.objects.get_for_model(QuestionAttempt)

        # Content Manager Permissions
        content_manager_permissions = [
            *Permission.objects.filter(content_type=study_material_ct),
            *Permission.objects.filter(content_type=subject_ct),
            *Permission.objects.filter(content_type=chapter_ct),
            *Permission.objects.filter(content_type=question_ct),
            *Permission.objects.filter(content_type=answer_ct),
            *Permission.objects.filter(content_type=exam_ct),
            *Permission.objects.filter(content_type=badge_ct),
            Permission.objects.get(
                content_type=exam_attempt_ct, codename="view_examattempt"
            ),
            Permission.objects.get(
                content_type=progress_ct, codename="view_chapterprogress"
            ),
            Permission.objects.get(
                content_type=question_attempt_ct, codename="view_questionattempt"
            ),
        ]
        content_manager_group.permissions.set(content_manager_permissions)

        # Academic Staff Permissions
        academic_staff_permissions = [
            Permission.objects.get(content_type=question_ct, codename="add_question"),
            Permission.objects.get(
                content_type=question_ct, codename="change_question"
            ),
            Permission.objects.get(content_type=question_ct, codename="view_question"),
            Permission.objects.get(content_type=exam_ct, codename="view_exam"),
            Permission.objects.get(
                content_type=exam_attempt_ct, codename="view_examattempt"
            ),
            Permission.objects.get(
                content_type=exam_attempt_ct, codename="change_examattempt"
            ),
            Permission.objects.get(
                content_type=progress_ct, codename="view_chapterprogress"
            ),
            Permission.objects.get(
                content_type=question_attempt_ct, codename="view_questionattempt"
            ),
            Permission.objects.get(
                content_type=study_material_ct, codename="view_studymaterial"
            ),
        ]
        academic_staff_group.permissions.set(academic_staff_permissions)

        # Student Support Staff Permissions
        support_staff_permissions = [
            Permission.objects.get(
                content_type=student_profile_ct, codename="view_studentprofile"
            ),
            Permission.objects.get(
                content_type=notification_ct, codename="add_notification"
            ),
            Permission.objects.get(
                content_type=notification_ct, codename="change_notification"
            ),
            Permission.objects.get(
                content_type=notification_ct, codename="view_notification"
            ),
            Permission.objects.get(
                content_type=study_material_ct, codename="view_studymaterial"
            ),
            Permission.objects.get(content_type=exam_ct, codename="view_exam"),
            Permission.objects.get(
                content_type=progress_ct, codename="view_chapterprogress"
            ),
        ]
        support_staff_group.permissions.set(support_staff_permissions)

        # Administrators get all permissions
        admin_permissions = Permission.objects.all()
        admin_group.permissions.set(admin_permissions)

        self.stdout.write(
            self.style.SUCCESS("Successfully set up user groups and permissions")
        )
