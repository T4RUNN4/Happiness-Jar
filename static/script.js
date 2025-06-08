document.addEventListener('DOMContentLoaded', function() {
    const html = '<!DOCTYPE ' + document.doctype.name + (document.doctype.publicId ? ' PUBLIC "' + document.doctype.publicId + '"' : '') + (!document.doctype.publicId && document.doctype.systemId ? ' SYSTEM' : '') + (document.doctype.systemId ? ' "' + document.doctype.systemId + '"' : '') + '>\n' + document.documentElement.outerHTML;
    document.querySelector('form[action="https://validator.w3.org/check"] > input[name="fragment"]').value = html;
});

document.addEventListener("DOMContentLoaded", function () {
    fetch("/mood-data")
        .then(response => response.json())
        .then(data => {
            const labels = Object.keys(data);
            const values = Object.values(data);

            const colors = [
                '#f9c74f', '#90be6d', '#f94144', '#577590', '#f3722c', '#43aa8b'
            ];

            new Chart(document.getElementById("moodChart"), {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: values,
                        backgroundColor: colors.slice(0, labels.length)
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        });
});
