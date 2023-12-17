document.addEventListener('DOMContentLoaded', ()=> {
    
    function get_data(){
        fetch()
    }

    //default
    load_chart()

    function load_chart(){
        console.log(dataset)
        console.log(labels)
        var ctx = document.getElementById('myChart').getContext('2d');

        var gradient = ctx.createLinearGradient(0, 0, 0, 400); // Create gradient (adjust as needed)
        gradient.addColorStop(0, 'red'); // Start color at red
        gradient.addColorStop(0.17, 'orange'); // Change color to orange at 17%
        gradient.addColorStop(0.33, 'yellow'); // Change color to yellow at 33%
        gradient.addColorStop(0.5, 'green'); // Change color to green at 50%
        gradient.addColorStop(0.67, 'blue'); // Change color to blue at 67%
        gradient.addColorStop(0.83, 'indigo'); // Change color to indigo at 83%
        gradient.addColorStop(1, 'violet'); // Change color to violet at 100%

        // Define your data
        var data = {
            labels: labels,
            datasets: [{
            label: "Balance",
            data: dataset,
            backgroundColor: 'rgba(0, 0, 0, 0)', // Set background color to transparent
            borderColor: gradient, // Line color
            borderWidth: 2, // Border width for the lines
            cubicInterpolationMode: 'monotone', // Set cubic interpolation mode to monotone

            }]
        };

        // Chart configuration
        var config = {
            type: 'line',
            data: data,
            options: {
            scales: {
                x: {
                ticks: {
                    color: 'white', // X-axis labels color
                },
                grid: {
                    color: 'white', // X-axis grid color
                },
                },
                y: {
                ticks: {
                    color: 'white', // Y-axis labels color
                },
                grid: {
                    color: 'white', // Y-axis grid color
                },
                },
            },
            plugins: {
                legend: {
                    labels: {
                        color: 'white', // This line changes the color of the 'Sample Data' label
                    },
                },
                tooltip: {
                backgroundColor: 'white', // Tooltip background color
                titleColor: 'black', // Tooltip title color
                bodyColor: 'black', // Tooltip body color
                callbacks: {
                    label: function (context) {
                        return context.dataset.label + ': ' + context.parsed.y; // Tooltip label color
                    },
                },
            },
        },
    },
};

        // Create the chart
        var myChart = new Chart(ctx, config);
    }

});