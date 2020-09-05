function openAttendanceModal() {
    var attendanceModal = document.getElementById("attendanceModal");
    attendanceModal.style.display = "block";
}

function openEmailModal() {
    var emailModal = document.getElementById("emailModal");
    emailModal.style.display = "block";
}

function closeAttendanceModal() {
    attendanceModal.style.display = "none";
}

function closeEmailModal() {
    emailModal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    try {
        if (event.target == attendanceModal) {
            attendanceModal.style.display = "none";
        }

        if (event.target == emailModal) {
            emailModal.style.display = "none";
        }
    } catch (error) {
        
    }
}

function removeStudent(url) {
    window.location.href = url;
}

function copyReport() {
    var element = document.getElementById("report");

    var range, selection, worked;

    if (document.body.createTextRange) {
        range = document.body.createTextRange();
        range.moveToElementText(element);
        range.select();
    } else if (window.getSelection) {
        selection = window.getSelection();        
        range = document.createRange();
        range.selectNodeContents(element);
        selection.removeAllRanges();
        selection.addRange(range);
    }

    try {
        document.execCommand('copy');
        alert('Report Successfully Copied!');
    }
    catch (err) {
        console.log(err);
        alert('unable to copy text');
    }
}