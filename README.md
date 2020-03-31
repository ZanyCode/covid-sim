<h3>Covid-Sim</h3>

A simple tool to visualize and compare Confirmed Cases, Deaths and Simulated Infections of Covid-19.
<br />Since the "Confirmed Cases" heavily depend on the number of tests performed, it is not a good indicator for the actual number of infections. Instead, the "Simulated Infections" feature is based on the number of deaths. <br/>
Assuming a known case fatality rate and infection rate, the "Simulated Infection" rate is calculated as follows:

For each datapoint containing the total number of deaths:
<ul> 
    <li>Calculate the total number of infections using deaths and case fatality rate (e.g. if there are 10 deaths with a cfr of 10%, we assume 100 infections in total)</li>   
    <li>Estimate the date of infection using the average time between infection and death (e.g if there are 10 deaths now with the average time between infection and death being 14 days, our estimated 100 total infections would have occured two weeks in the past)</li>
    <li>Calculate how far the virus has spread since the infection occured using the infection rate and average time between infection and death (e.g. if the number of infections doubles every 3 days, and our 100 infections occurred 12 days ago, the number of infections would have doubled 4 times. Consequently, we now would have 1600 infections)
</ul>

The parameters necessary for the estimation can be set freely using the web frontend.

<img height="350px" align="right" src="/docs/countries_by_feature.PNG">
