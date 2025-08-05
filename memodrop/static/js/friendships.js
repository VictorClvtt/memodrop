function changeSection(tableId, buttonId) {
    const tableIds = ['friends-section', 'other-users-section'];
    const buttonIds = ['friends-btn', 'other-users-btn'];

    for (let i = 0; i < tableIds.length; i++) {
        document.getElementById(tableIds[i]).classList.add('d-none');
        document.getElementById(buttonIds[i]).classList.remove('active-table-button');
    }

    document.getElementById(tableId).classList.remove('d-none');
    document.getElementById(buttonId).classList.add('active-table-button');
}