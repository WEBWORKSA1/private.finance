/* Multi-step advisor-matching form */
(function(){
  "use strict";
  var f=document.getElementById("lead-form");if(!f)return;
  var steps=[].slice.call(f.querySelectorAll(".step")),i=0,bar=document.getElementById("lead-bar"),lab=document.getElementById("lead-step");
  function show(n){
    i=Math.max(0,Math.min(n,steps.length-1));
    steps.forEach(function(s,k){s.classList.toggle("active",k===i);});
    if(bar)bar.style.width=((i+1)/steps.length*100)+"%";
    if(lab)lab.textContent="Step "+(i+1)+" of "+steps.length;
    var first=steps[i].querySelector("input,select,textarea");if(first&&i>0)first.focus({preventScroll:true});
    f.scrollIntoView({behavior:"smooth",block:"start"});
  }
  function valid(){
    var s=steps[i],ok=true;
    s.querySelectorAll("[data-req-group]").forEach(function(g){if(!g.querySelector("input:checked"))ok=false;});
    s.querySelectorAll("input,select,textarea").forEach(function(el){if(el.required&&!el.checkValidity())ok=false;});
    var m=s.querySelector(".step-err");
    if(!ok){if(m)m.textContent="Please choose an option to continue.";var bad=s.querySelector("input:invalid,select:invalid");if(bad&&bad.reportValidity)bad.reportValidity();}
    else if(m)m.textContent="";
    return ok;
  }
  f.addEventListener("click",function(e){
    if(e.target.closest("[data-next]")){e.preventDefault();if(valid())show(i+1);}
    if(e.target.closest("[data-prev]")){e.preventDefault();show(i-1);}
  });
  f.addEventListener("change",function(e){
    if(e.target.type==="radio"&&e.target.closest("[data-auto-next]")){setTimeout(function(){if(valid())show(i+1);},250);}
  });
  /* prefill from homepage teaser or calculators */
  var p=new URLSearchParams(location.search);
  ["goal","assets","source"].forEach(function(k){
    var val=p.get(k);if(!val)return;
    var r=f.querySelector('input[name="'+k+'"][value="'+val+'"]');if(r)r.checked=true;
    var h=f.querySelector('input[type=hidden][name="'+k+'"]');if(h)h.value=val;
  });
  try{var hs=localStorage.getItem("pf_health_score");if(hs){var el=document.getElementById("lead-health");if(el)el.value=hs;}}catch(e){}
  if(p.get("goal")&&p.get("assets")){show(2);}else show(0);
  f.addEventListener("submit",function(e){
    e.preventDefault();if(!valid())return;
    var a=(f.querySelector('input[name="assets"]:checked')||{}).value||"";
    var tier={"under-50k":"C","50k-250k":"B","250k-1m":"A","1m-5m":"A+","5m-plus":"A++"}[a]||"C";
    PF.submit(f,{lead_tier:tier,_subject:"New advisor-match lead ["+tier+"]"}).then(function(ok){
      if(ok){steps.forEach(function(s){s.classList.remove("active");});document.getElementById("lead-done").style.display="block";if(bar)bar.style.width="100%";if(lab)lab.textContent="Done";}
    });
  });
})();
