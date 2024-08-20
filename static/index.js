   document.querySelectorAll('.delete-btn').forEach(function(button) {
         button.addEventListener('click', function(event) {
             event.preventDefault();
             if (confirm("Bạn có chắc muốn xóa sinh viên này không?")) {
                 window.location.href = button.getAttribute('href'); // Proceed with the delete action
             }
         });
     });

