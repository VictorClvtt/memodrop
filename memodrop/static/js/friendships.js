function changeSection(sectionId, buttonId) {
        const sections = document.querySelectorAll('main > section');
        const buttons = document.querySelectorAll('button');

        sections.forEach(section => section.classList.add('d-none'));
        buttons.forEach(button => button.classList.remove('active-table-button'));

        document.getElementById(sectionId).classList.remove('d-none');
        document.getElementById(buttonId).classList.add('active-table-button');
}