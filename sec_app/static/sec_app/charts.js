const ctx1 = document.getElementById('myChart3');
const ctx2 = document.getElementById('myChart4');
const ctx3 = document.getElementById('myChart5');

fetch('http://127.0.0.1:8000/years/')
  .then((response) => response.json())
  .then((data) => {console.log(data.graph1_data['2010'])
    //chart 1
    new Chart(ctx1, {
          type: 'line',
          data: {
            labels: [2010,2012,2014,2016,2018,2020,2022],
            datasets: [{
              label: 'Yıllara Göre Zaaf Sayıları',
              data: [data.graph1_data['2010'], data.graph1_data['2012'], data.graph1_data['2014'], data.graph1_data['2016'], data.graph1_data['2018'], data.graph1_data['2020'],data.graph1_data['2022']],
              
            }]
          },
          options: {
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });

        //chart 2
        new Chart(ctx2, {
          type: 'pie',
          data: {
            labels: ["Critical", "High", "Medium", "Low",],
            datasets: [{
              label: 'Zaafların Toplam Oranı',
              data: [data.graph2_data['4'], data.graph2_data['3'], data.graph2_data['2'], data.graph2_data['1']],
              borderWidth: 3
            }]
          },
          options: {
          }
        });


        //chart 3
        new Chart(ctx3, {
          type: 'bar',
          data: {
            labels: ["Critical", "High", "Medium", "Low"],
            datasets: [{
              label: '2022 Zaafları Risk Düzeyleri',
              data: [data.graph3_data['4'], data.graph3_data['3'], data.graph3_data['2'], data.graph3_data['1']],
              borderWidth: 3
            }]
          },
          options: {
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
        
        
  });

    
      

    
      
    
      
