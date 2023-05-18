

function calculatePrice() {
    let price_value = 0
    let kilometer = document.getElementById('kilometer').value
    let priceperkm = document.getElementById('one_kilometer_price').value
    price_value = kilometer * priceperkm

    document.getElementById('price').value = price_value

}






$(".dep_arv_date_time").on("change", function() {
           
            var departure_date =    new Date(     $("#departure_date").val())
            var departure_time =   $("#departure_time").val()
            var arrival_date= new Date($("#arrival_date").val())
            var arrival_time=$("#arrival_time").val()

            let difference = arrival_date.getTime() - departure_date.getTime();
            let TotalDays = Math.ceil(difference / (1000 * 3600 * 24));
           
            console.log(TotalDays,"Days")
   
            var diff = 0 ;
            var hr;
            var sec;
            var min;
            if (departure_time && arrival_time) {
              smon = ConvertToSeconds(departure_time);
              fmon = ConvertToSeconds(arrival_time);
              diff = Math.abs( fmon - smon ) ;
              secondsTohhmmss(diff)
            }
          
            function ConvertToSeconds(time) {
              var splitTime = time.split(":");
              return splitTime[0] * 3600 + splitTime[1] * 60;
            }
          
            function secondsTohhmmss(secs) {
              var hours = parseInt(secs / 3600);
              var seconds = parseInt(secs % 3600);
              var minutes = parseInt(seconds / 60) ;
              hr=hours;
              sec=seconds;
              min=minutes;

         

                    
                
             
            }
            document.getElementById('duration').value=String(TotalDays) + " Days" + " " + String(hr)+" Hours" + " " + String(min)+" Minutes"+ " " +String(sec) +" Second" 
         

            
           
 });
