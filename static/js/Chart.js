<script>
    const classCtx = document.getElementById('classChart').getContext('2d');
    new Chart(classCtx, {
        type: 'bar',
    data: {
        labels: {{ class_labels| tojson}},
    datasets: [{
        label: 'Books Issued (Students)',
    data: {{ class_data| tojson}},
    backgroundColor: '#2a9d8f',
    borderRadius: 10
            }]
        },
    options: {
        responsive: true,
    plugins: {legend: {display: true } },
    animation: {
        duration: 1200,
    easing: 'easeInOutBounce'
            },
    scales: {
        y: {beginAtZero: true }
            }
        }
    });

    // 🧑‍🏫 Teacher Subject Chart
    const teacherCanvas = document.createElement('canvas');
    teacherCanvas.id = 'teacherChart';
    document.querySelector('.chart-container').appendChild(teacherCanvas);

    const teacherCtx = teacherCanvas.getContext('2d');
    new Chart(teacherCtx, {
        type: 'bar',
    data: {
        labels: {{ teacher_labels| tojson}},
    datasets: [{
        label: 'Books Issued (Teachers)',
    data: {{ teacher_data| tojson}},
    backgroundColor: '#ffbe0b',
    borderRadius: 10
            }]
        },
    options: {
        responsive: true,
    plugins: {legend: {display: true } },
    animation: {
        duration: 1500,
    easing: 'easeInOutBack'
            },
    scales: {
        y: {beginAtZero: true }
            }
        }
    });
</script>
