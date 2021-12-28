<ul class="nav-main">
    <li>
        <a class="active" href="{{ route('admin.index') }}">
            <i class="si si-cup"></i>
            <span class="sidebar-mini-hide">Главная</span>
        </a>
    </li>
    <li class="nav-main-heading">
        <span class="sidebar-mini-visible">Р</span>
        <span class="sidebar-mini-hidden">Разделы</span>
    </li>
    <li>
        <a href="{{ route('admin.categories.index') }}">
            <i class="si si-list"></i>
            <span class="sidebar-mini-hide">Категории</span>
        </a>
    </li>
    <li>
        <a href="{{ route('admin.vacations.index') }}">
            <i class="si si-docs"></i>
            <span class="sidebar-mini-hide">Вакансии</span>
        </a>
    </li>
    <li>
        <a href="{{ route('admin.resumes.index') }}">
            <i class="si si-docs"></i>
            <span class="sidebar-mini-hide">Резюме</span>
        </a>
    </li>
    <li>
        <a href="{{ route('admin.referral.index') }}">
            <i class="si si-users"></i>
            <span class="sidebar-mini-hide">Реферальная система</span>
        </a>
    </li>
    <li>
        <a href="{{ route('admin.users.index') }}">
            <i class="si si-user"></i>
            <span class="sidebar-mini-hide">Пользователи</span>
        </a>
    </li>
    <li>
        <a href="{{ route('admin.telegram.index') }}">
            <i class="fa fa-send-o"></i>
            <span class="sidebar-mini-hide">Telegram</span>
        </a>
    </li>
    <li>
        <a href="{{ route('admin.settings.index') }}">
            <i class="si si-settings"></i>
            <span class="sidebar-mini-hide">Настройки</span>
        </a>
    </li>
</ul>
