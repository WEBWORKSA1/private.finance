/* Private.Finance calculators — every number is computed in your browser. Nothing is sent anywhere. */
(function(){
  "use strict";
  var PF=window.PF||{};
  var $=function(s,r){return (r||document).querySelector(s);};
  var $$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s));};
  var fmt=function(n,d){return PF.fmt?PF.fmt(n,d):Math.round(n).toLocaleString();};
  function v(id){var el=document.getElementById(id);if(!el)return 0;var x=parseFloat(String(el.value).replace(/[^0-9.\-]/g,""));return isFinite(x)?x:0;}
  function set(id,t){var el=document.getElementById(id);if(el)el.textContent=t;}
  function compact(n){var a=Math.abs(n),s=n<0?"-":"";if(a>=1e9)return s+(a/1e9).toFixed(1)+"B";if(a>=1e6)return s+(a/1e6).toFixed(1)+"M";if(a>=1e3)return s+(a/1e3).toFixed(0)+"k";return s+Math.round(a);}
  function css(name){return getComputedStyle(document.documentElement).getPropertyValue(name).trim()||"#0f5c4d";}

  /* ---------- tiny canvas chart ---------- */
  function chart(canvas,o){
    if(!canvas)return;
    var dpr=window.devicePixelRatio||1,w=canvas.clientWidth,h=canvas.clientHeight;
    canvas.width=w*dpr;canvas.height=h*dpr;
    var c=canvas.getContext("2d");c.setTransform(dpr,0,0,dpr,0,0);c.clearRect(0,0,w,h);
    var txt=css("--muted"),grid=css("--line");
    c.font="12px "+css("--f-mono");
    if(o.type==="donut"){
      var tot=o.series.reduce(function(s,x){return s+Math.max(0,x.value);},0)||1,ang=-Math.PI/2,cx=w/2,cy=h/2,r=Math.min(w,h)/2-10;
      o.series.forEach(function(x){var a=Math.max(0,x.value)/tot*Math.PI*2;c.beginPath();c.moveTo(cx,cy);c.arc(cx,cy,r,ang,ang+a);c.closePath();c.fillStyle=x.color;c.fill();ang+=a;});
      c.beginPath();c.arc(cx,cy,r*.6,0,Math.PI*2);c.fillStyle=css("--card");c.fill();
      c.fillStyle=css("--text");c.textAlign="center";c.font="600 15px "+css("--f-mono");c.fillText(o.center||"",cx,cy+5);return;
    }
    var L=56,R=12,T=12,B=26,pw=w-L-R,ph=h-T-B,n=o.labels.length;
    var max=0;
    if(o.type==="stack"){for(var i=0;i<n;i++){var s=0;o.series.forEach(function(x){s+=Math.max(0,x.data[i]||0);});max=Math.max(max,s);}}
    else o.series.forEach(function(x){x.data.forEach(function(d){max=Math.max(max,d||0);});});
    max=max||1;var step=Math.pow(10,Math.floor(Math.log10(max)));var nice=Math.ceil(max/step)*step;if(nice/step<3)nice=Math.ceil(max/(step/2))*(step/2);max=nice;
    c.strokeStyle=grid;c.fillStyle=txt;c.textAlign="right";c.lineWidth=1;
    for(var g=0;g<=4;g++){var y=T+ph-ph*g/4;c.beginPath();c.moveTo(L,y);c.lineTo(w-R,y);c.stroke();c.fillText(compact(max*g/4),L-8,y+4);}
    c.textAlign="center";var every=Math.ceil(n/8);
    o.labels.forEach(function(lb,i){if(i%every===0||(i===n-1&&(n-1)%every>=every*0.6)){var x=L+(n===1?pw/2:pw*i/(n-1));if(o.type==="stack")x=L+pw*(i+.5)/n;c.fillText(lb,x,h-8);}});
    if(o.type==="stack"){
      var bw=Math.max(2,pw/n*.7);
      for(var j=0;j<n;j++){var base=0,x=L+pw*(j+.5)/n-bw/2;o.series.forEach(function(sr){var val=Math.max(0,sr.data[j]||0),bh=ph*val/max;c.fillStyle=sr.color;c.fillRect(x,T+ph-base-bh,bw,bh);base+=bh;});}
    } else {
      o.series.forEach(function(sr){
        c.beginPath();c.lineWidth=sr.width||2.5;c.strokeStyle=sr.color;if(sr.dash)c.setLineDash(sr.dash);else c.setLineDash([]);
        sr.data.forEach(function(d,i){var x=L+(n===1?pw/2:pw*i/(n-1)),y=T+ph-ph*(d||0)/max;i?c.lineTo(x,y):c.moveTo(x,y);});
        c.stroke();
        if(sr.fill){c.lineTo(L+pw,T+ph);c.lineTo(L,T+ph);c.closePath();c.globalAlpha=.12;c.fillStyle=sr.color;c.fill();c.globalAlpha=1;}
      });
      c.setLineDash([]);
    }
  }
  function legend(el,series){if(!el)return;el.innerHTML=series.map(function(s){return '<span><i style="background:'+s.color+'"></i>'+s.name+'</span>';}).join("");}
  var C1=function(){return "#0f5c4d";},C2=function(){return "#c9a227";},C3=function(){return "#b4443a";},C4=function(){return "#2c6e9b";};

  /* ---------- core math ---------- */
  function fv(P,pmt,rate,years,n){ // monthly contributions, compounding n/yr
    n=n||12;var bal=P,out=[{y:0,bal:P,contrib:P}],contrib=P,months=Math.round(years*12);
    var mRate=Math.pow(1+rate/100/n,n/12)-1;
    for(var m=1;m<=months;m++){bal=bal*(1+mRate)+pmt;contrib+=pmt;if(m%12===0)out.push({y:m/12,bal:bal,contrib:contrib});}
    return out;
  }
  function payment(P,rate,months){var r=rate/100/12;return r===0?P/months:P*r/(1-Math.pow(1+r,-months));}

  var calcs={};

  calcs["compound-interest"]=function(){
    var rows=fv(v("ci-p"),v("ci-m"),v("ci-r"),Math.max(1,v("ci-y")),v("ci-n")||12),last=rows[rows.length-1];
    set("ci-fv",fmt(last.bal));set("ci-c",fmt(last.contrib));set("ci-i",fmt(last.bal-last.contrib));
    set("ci-x",(last.contrib?last.bal/last.contrib:0).toFixed(2)+"×");
    var s=[{name:"Your contributions",color:C1(),data:rows.map(function(r){return r.contrib;})},{name:"Interest earned",color:C2(),data:rows.map(function(r){return r.bal-r.contrib;})}];
    chart($("#ci-chart"),{type:"stack",labels:rows.map(function(r){return "Y"+r.y;}),series:s});legend($("#ci-legend"),s);
    var tb=$("#ci-table");if(tb)tb.innerHTML=rows.filter(function(r,i){return i>0;}).map(function(r){return "<tr><td>"+r.y+"</td><td class=num>"+fmt(r.contrib)+"</td><td class=num>"+fmt(r.bal-r.contrib)+"</td><td class=num><b>"+fmt(r.bal)+"</b></td></tr>";}).join("");
  };

  calcs["retirement"]=function(){
    var age=v("rt-age"),ret=Math.max(age+1,v("rt-ret")),yrs=ret-age,inf=v("rt-inf")/100,wr=Math.max(.5,v("rt-wr"))/100;
    var income=v("rt-inc"),futureIncome=income*Math.pow(1+inf,yrs),target=futureIncome/wr;
    var rows=fv(v("rt-sav"),v("rt-m"),v("rt-r"),yrs,12),proj=rows[rows.length-1].bal;
    var gap=target-proj,r=Math.pow(1+v("rt-r")/100,1/12)-1,months=yrs*12;
    var growthOfCurrent=v("rt-sav")*Math.pow(1+r,months);
    var need=r===0?(target-growthOfCurrent)/months:(target-growthOfCurrent)*r/(Math.pow(1+r,months)-1);
    set("rt-target",fmt(target));set("rt-proj",fmt(proj));
    set("rt-gap",gap>0?fmt(gap)+" short":fmt(-gap)+" ahead");
    var gapEl=document.getElementById("rt-gap");if(gapEl)gapEl.style.color=gap>0?"#b4443a":"#137a66";
    set("rt-need",need>0?fmt(need)+"/mo":"On track 🎉");
    set("rt-today",fmt(target/Math.pow(1+inf,yrs)));
    var pct=Math.min(100,proj/target*100);set("rt-pct",pct.toFixed(0)+"%");
    var bar=document.getElementById("rt-bar");if(bar)bar.style.width=pct+"%";
    var s=[{name:"Projected savings",color:C1(),data:rows.map(function(x){return x.bal;}),fill:true},{name:"Target nest egg",color:C2(),data:rows.map(function(){return target;}),dash:[6,4]}];
    chart($("#rt-chart"),{type:"line",labels:rows.map(function(x){return String(age+x.y);}),series:s});legend($("#rt-legend"),s);
  };

  calcs["mortgage"]=function(){
    var price=v("mg-price"),dpPct=v("mg-dp"),dp=price*dpPct/100,P=price-dp,rate=v("mg-rate"),yrs=Math.max(1,v("mg-term")),months=yrs*12;
    var pi=payment(P,rate,months),tax=price*v("mg-tax")/100/12,ins=v("mg-ins")/12,pmiRate=dpPct<20?v("mg-pmi"):0;
    var r=rate/100/12,bal=P,totalInt=0,pmiMonths=0,rows=[],yrBal=[P],yrInt=0,yrPrin=0;
    for(var m=1;m<=months;m++){
      var it=bal*r,pr=pi-it;bal=Math.max(0,bal-pr);totalInt+=it;yrInt+=it;yrPrin+=pr;
      if(pmiRate>0&&(bal+pr)/price>0.78)pmiMonths++;
      if(m%12===0){rows.push({y:m/12,int:yrInt,prin:yrPrin,bal:bal});yrBal.push(bal);yrInt=0;yrPrin=0;}
    }
    var pmi=pmiRate>0?P*pmiRate/100/12:0;
    set("mg-pi",fmt(pi));set("mg-total",fmt(pi+tax+ins+pmi));set("mg-int",fmt(totalInt));set("mg-loan",fmt(P));
    set("mg-pmi-out",pmi>0?fmt(pmi)+"/mo for ~"+Math.ceil(pmiMonths/12)+" yrs":"None (20%+ down)");
    set("mg-dp-out",fmt(dp));
    var s=[{name:"Principal paid",color:C1(),data:rows.map(function(x){return x.prin;})},{name:"Interest paid",color:C2(),data:rows.map(function(x){return x.int;})}];
    chart($("#mg-chart"),{type:"stack",labels:rows.map(function(x){return "Y"+x.y;}),series:s});legend($("#mg-legend"),s);
    var tb=$("#mg-table");if(tb)tb.innerHTML=rows.map(function(x){return "<tr><td>"+x.y+"</td><td class=num>"+fmt(x.prin)+"</td><td class=num>"+fmt(x.int)+"</td><td class=num>"+fmt(x.bal)+"</td></tr>";}).join("");
  };

  /* debt payoff: avalanche vs snowball */
  function simulate(debts,extra,method){
    var ds=debts.map(function(d){return {n:d.n,b:d.b,r:d.r/100/12,m:d.m};}).filter(function(d){return d.b>0;});
    var order=ds.slice().sort(method==="avalanche"?function(a,b){return b.r-a.r;}:function(a,b){return a.b-b.b;}).map(function(d){return d.n;});
    var budget=ds.reduce(function(s,d){return s+d.m;},0)+extra,month=0,interest=0,series=[ds.reduce(function(s,d){return s+d.b;},0)],paidOff=[];
    while(ds.some(function(d){return d.b>0.005;})&&month<600){
      month++;var avail=budget;
      ds.forEach(function(d){if(d.b>0){var i=d.b*d.r;interest+=i;d.b+=i;}});
      ds.forEach(function(d){if(d.b>0){var p=Math.min(d.m,d.b);d.b-=p;avail-=p;}});
      for(var k=0;k<order.length&&avail>0.005;k++){var t=ds.filter(function(d){return d.n===order[k];})[0];if(t&&t.b>0){var p2=Math.min(avail,t.b);t.b-=p2;avail-=p2;}}
      ds.forEach(function(d){if(d.b<=0.005&&paidOff.indexOf(d.n)<0){d.b=0;paidOff.push(d.n);}});
      series.push(ds.reduce(function(s,d){return s+d.b;},0));
    }
    return {months:month,interest:interest,series:series,order:paidOff,stuck:month>=600};
  }
  calcs["debt-payoff"]=function(){
    var debts=$$("#dp-rows tr").map(function(tr,i){var q=function(s){var x=parseFloat(tr.querySelector(s).value);return isFinite(x)?x:0;};return {n:tr.querySelector(".d-n").value||("Debt "+(i+1)),b:q(".d-b"),r:q(".d-r"),m:q(".d-m")};});
    var extra=v("dp-extra"),a=simulate(debts,extra,"avalanche"),s=simulate(debts,extra,"snowball");
    function yrs(m){return Math.floor(m/12)+" yr "+(m%12)+" mo";}
    set("dp-a-time",a.stuck?"50+ yrs":yrs(a.months));set("dp-a-int",fmt(a.interest));
    set("dp-s-time",s.stuck?"50+ yrs":yrs(s.months));set("dp-s-int",fmt(s.interest));
    set("dp-save",fmt(Math.max(0,s.interest-a.interest)));
    set("dp-a-order",a.order.join(" → ")||"—");set("dp-s-order",s.order.join(" → ")||"—");
    var warn=document.getElementById("dp-warn");if(warn)warn.style.display=(a.stuck||s.stuck)?"block":"none";
    var len=Math.max(a.series.length,s.series.length),lab=[];for(var i=0;i<len;i++)lab.push(i%12===0?"Y"+(i/12):"");
    var pad=function(arr){var o=arr.slice();while(o.length<len)o.push(0);return o;};
    var sr=[{name:"Avalanche (highest rate first)",color:C1(),data:pad(a.series)},{name:"Snowball (smallest balance first)",color:C3(),data:pad(s.series),dash:[6,4]}];
    chart($("#dp-chart"),{type:"line",labels:lab.map(function(l,i){return i%12===0?String(i/12):"";}),series:sr});legend($("#dp-legend"),sr);
  };
  function debtRow(n,b,r,m){var tr=document.createElement("tr");tr.innerHTML='<td><input class="d-n" type="text" value="'+n+'" aria-label="Debt name"></td><td><input class="d-b" type="number" min="0" value="'+b+'" aria-label="Balance"></td><td><input class="d-r" type="number" min="0" step="0.1" value="'+r+'" aria-label="APR %"></td><td><input class="d-m" type="number" min="0" value="'+m+'" aria-label="Minimum payment"></td><td><button type="button" class="icon-btn d-x" aria-label="Remove debt">×</button></td>';return tr;}

  calcs["budget"]=function(){
    var inc=v("bg-inc"),n=inc*v("bg-np")/100,w=inc*v("bg-wp")/100,s=inc*v("bg-sp")/100,tot=v("bg-np")+v("bg-wp")+v("bg-sp");
    set("bg-n",fmt(n));set("bg-w",fmt(w));set("bg-s",fmt(s));set("bg-np-o",v("bg-np")+"%");set("bg-wp-o",v("bg-wp")+"%");set("bg-sp-o",v("bg-sp")+"%");
    set("bg-tot",tot+"%");var t=document.getElementById("bg-tot");if(t)t.style.color=tot===100?"":"#b4443a";
    set("bg-yr",fmt(s*12));
    var an=v("bg-an"),aw=v("bg-aw"),as=v("bg-as"),fb=$("#bg-feedback");
    if(fb){
      if(an+aw+as>0){
        var tips=[];
        if(an>n)tips.push("Needs are "+fmt(an-n)+" over target — housing and transport are usually the biggest levers.");
        if(aw>w)tips.push("Wants are "+fmt(aw-w)+" over — try a 30-day pause on one category.");
        if(as<s)tips.push("Savings are "+fmt(s-as)+" under target — automate a transfer on payday.");
        if(!tips.length)tips.push("You're at or better than the 50/30/20 targets. Consider raising your savings rate.");
        fb.innerHTML="<ul class='list-check'>"+tips.map(function(x){return "<li>"+x+"</li>";}).join("")+"</ul>";
      } else fb.innerHTML="<p class='muted'>Enter your actual monthly spending to compare against the targets.</p>";
    }
    var sr=[{name:"Needs",color:C1(),value:n},{name:"Wants",color:C2(),value:w},{name:"Savings & debt",color:C4(),value:s}];
    chart($("#bg-chart"),{type:"donut",series:sr,center:fmt(inc)});legend($("#bg-legend"),sr);
  };

  calcs["emergency-fund"]=function(){
    var exp=$$(".ef-exp").reduce(function(s,el){var x=parseFloat(el.value);return s+(isFinite(x)?x:0);},0);
    var months=v("ef-months"),goal=exp*months,have=v("ef-have"),save=v("ef-save"),left=Math.max(0,goal-have);
    set("ef-total",fmt(exp));set("ef-goal",fmt(goal));set("ef-left",fmt(left));set("ef-months-o",months+" months");
    set("ef-time",left===0?"Fully funded ✓":save>0?Math.ceil(left/save)+" months":"Add a monthly amount");
    var pct=goal?Math.min(100,have/goal*100):0;set("ef-pct",pct.toFixed(0)+"%");var b=document.getElementById("ef-bar");if(b)b.style.width=pct+"%";
  };
  function efSuggest(){var s=document.getElementById("ef-stab");if(!s)return;var m={stable:3,average:6,variable:9,self:12}[s.value]||6;var el=document.getElementById("ef-months");if(el){el.value=m;}}

  calcs["loan"]=function(){
    var P=v("ln-p"),rate=v("ln-r"),months=Math.max(1,Math.round(v("ln-t")*(document.getElementById("ln-unit")&&document.getElementById("ln-unit").value==="months"?1:12)));
    var pm=payment(P,rate,months),tot=pm*months,int=tot-P;
    set("ln-pm",fmt(pm,2));set("ln-int",fmt(int));set("ln-tot",fmt(tot));set("ln-n",months+" payments");
    var sr=[{name:"Principal",color:C1(),value:P},{name:"Interest",color:C2(),value:int}];
    chart($("#ln-chart"),{type:"donut",series:sr,center:(P?int/P*100:0).toFixed(0)+"% extra"});legend($("#ln-legend"),sr);
  };

  calcs["net-worth"]=function(){
    var sum=function(cls){return $$(cls).reduce(function(s,el){var x=parseFloat(el.value);return s+(isFinite(x)?x:0);},0);};
    var a=sum(".nw-a"),l=sum(".nw-l"),nw=a-l;
    set("nw-a",fmt(a));set("nw-l",fmt(l));set("nw-nw",fmt(nw));set("nw-ratio",a?(l/a*100).toFixed(0)+"%":"—");
    var e=document.getElementById("nw-nw");if(e)e.style.color=nw<0?"#ffb4a8":"";
    var sr=[{name:"Assets",color:C1(),value:a},{name:"Liabilities",color:C3(),value:l}];
    chart($("#nw-chart"),{type:"donut",series:sr,center:fmt(nw)});legend($("#nw-legend"),sr);
    if(document.getElementById("nw-remember")&&document.getElementById("nw-remember").checked){
      var data={};$$(".nw-a,.nw-l").forEach(function(el){data[el.id]=el.value;});PF.store.set("networth",data);
    }
  };
  function nwRestore(){var d=PF.store.get("networth",null);if(d){Object.keys(d).forEach(function(k){var el=document.getElementById(k);if(el)el.value=d[k];});var c=document.getElementById("nw-remember");if(c)c.checked=true;}}

  calcs["savings-goal"]=function(){
    var goal=v("sg-goal"),have=v("sg-have"),r=Math.pow(1+v("sg-r")/100,1/12)-1,months=Math.max(1,Math.round(v("sg-y")*12));
    var grown=have*Math.pow(1+r,months),need=Math.max(0,goal-grown),pm=r===0?need/months:need*r/(Math.pow(1+r,months)-1);
    set("sg-pm",fmt(pm));set("sg-wk",fmt(pm*12/52));set("sg-int",fmt(Math.max(0,goal-have-pm*months)));
    var rows=fv(have,pm,v("sg-r"),months/12,12);
    var sr=[{name:"Balance",color:C1(),data:rows.map(function(x){return x.bal;}),fill:true},{name:"Goal",color:C2(),data:rows.map(function(){return goal;}),dash:[6,4]}];
    chart($("#sg-chart"),{type:"line",labels:rows.map(function(x){return "Y"+x.y;}),series:sr});legend($("#sg-legend"),sr);
  };

  calcs["inflation"]=function(){
    var amt=v("in-amt"),r=v("in-r")/100,y=Math.max(1,v("in-y"));
    var future=amt*Math.pow(1+r,y),power=amt/Math.pow(1+r,y);
    set("in-fut",fmt(future));set("in-pow",fmt(power));set("in-loss",(100-power/amt*100).toFixed(1)+"%");
    var lab=[],a=[],b=[];for(var i=0;i<=y;i++){lab.push("Y"+i);a.push(amt*Math.pow(1+r,i));b.push(amt/Math.pow(1+r,i));}
    var sr=[{name:"Cost of the same basket",color:C3(),data:a},{name:"Purchasing power of today's money",color:C1(),data:b,fill:true}];
    chart($("#in-chart"),{type:"line",labels:lab,series:sr});legend($("#in-legend"),sr);
  };

  /* ---------- wiring ---------- */
  var root=$("[data-calc]");
  if(root){
    var name=root.getAttribute("data-calc"),run=function(){try{calcs[name]();}catch(e){if(window.console)console.warn(e);}};
    if(name==="debt-payoff"){
      var body=$("#dp-rows");
      [["Credit card",6500,22.9,160],["Car loan",12000,7.5,280],["Personal loan",4000,12,120]].forEach(function(d){body.appendChild(debtRow(d[0],d[1],d[2],d[3]));});
      $("#dp-add").addEventListener("click",function(){body.appendChild(debtRow("New debt",1000,10,50));run();});
      body.addEventListener("click",function(e){if(e.target.closest(".d-x")){e.target.closest("tr").remove();run();}});
    }
    if(name==="emergency-fund"){var st=$("#ef-stab");if(st)st.addEventListener("change",function(){efSuggest();run();});}
    if(name==="net-worth"){nwRestore();var rm=$("#nw-remember");if(rm)rm.addEventListener("change",function(){if(!rm.checked)PF.store.set("networth",null);run();});var clr=$("#nw-clear");if(clr)clr.addEventListener("click",function(){$$(".nw-a,.nw-l").forEach(function(el){el.value="";});PF.store.set("networth",null);run();});}
    root.addEventListener("input",function(e){
      var o=e.target.id&&document.querySelector('output[for="'+e.target.id+'"]');if(o)o.textContent=e.target.value+(o.dataset.suffix||"");
      run();
    });
    $$("input[type=range]",root).forEach(function(r){var o=document.querySelector('output[for="'+r.id+'"]');if(o)o.textContent=r.value+(o.dataset.suffix||"");});
    document.addEventListener("pf:currency",run);
    window.addEventListener("resize",function(){clearTimeout(window._pfr);window._pfr=setTimeout(run,150);});
    run();
    /* share link with inputs in the URL hash (stays on the device, nothing uploaded) */
    var share=$("#calc-share");
    if(share)share.addEventListener("click",function(){
      var q=$$("input[id],select[id]",root).filter(function(i){return i.type!=="checkbox";}).map(function(i){return i.id+"="+encodeURIComponent(i.value);}).join("&");
      var url=location.href.split("#")[0]+"#"+q;
      if(navigator.clipboard)navigator.clipboard.writeText(url).then(function(){share.textContent="Link copied ✓";setTimeout(function(){share.textContent="Copy shareable link";},2000);});
      else prompt("Copy this link",url);
    });
    if(location.hash.length>1){location.hash.slice(1).split("&").forEach(function(p){var kv=p.split("="),el=document.getElementById(kv[0]);if(el&&root.contains(el))el.value=decodeURIComponent(kv[1]||"");});run();}
    var pr=$("#calc-print");if(pr)pr.addEventListener("click",function(){window.print();});
  }

  /* ---------- home hero widget ---------- */
  var hw=$("#hero-widget");
  if(hw){
    var hrun=function(){var rows=fv(0,v("hw-m"),v("hw-r"),v("hw-y"),12),last=rows[rows.length-1];
      $$("output",hw).forEach(function(o){var i=document.getElementById(o.getAttribute("for"));if(i)o.textContent=(o.dataset.pre==="cur"?fmt(+i.value):i.value)+(o.dataset.suffix||"");});
      set("hw-out",fmt(last.bal));set("hw-int",fmt(last.bal-last.contrib));
      chart($("#hw-chart"),{type:"line",labels:rows.map(function(x){return "Y"+x.y;}),series:[{name:"Balance",color:C1(),data:rows.map(function(x){return x.bal;}),fill:true},{name:"Contributed",color:C2(),data:rows.map(function(x){return x.contrib;}),dash:[5,4]}]});};
    hw.addEventListener("input",hrun);document.addEventListener("pf:currency",hrun);window.addEventListener("resize",hrun);hrun();
  }

  /* ---------- Financial Health Score quiz ---------- */
  var qz=$("#quiz");
  if(qz){
    var qs=$$(".quiz-q",qz),cur=0,bar=$("#quiz-bar");
    var show=function(i){qs.forEach(function(q,k){q.classList.toggle("active",k===i);});if(bar)bar.style.width=(i/qs.length*100)+"%";};
    qz.addEventListener("change",function(e){
      if(e.target.type!=="radio")return;
      setTimeout(function(){cur++;if(cur<qs.length)show(cur);else finish();},220);
    });
    var finish=function(){
      var score=0,weak=[];
      qs.forEach(function(q){var c=q.querySelector("input:checked");var p=c?+c.value:0;score+=p;if(p<10&&q.dataset.fix)weak.push(q.dataset.fix);});
      score=Math.round(score/(qs.length*20)*100);
      if(bar)bar.style.width="100%";
      qs.forEach(function(q){q.classList.remove("active");});
      var band=score>=80?["Excellent","You're in the top tier of financial resilience. Next step: optimize taxes, fees and estate planning."]:score>=60?["Solid","Strong foundations with a few gaps worth closing."]:score>=40?["Building","You have momentum — focus on the two weakest areas below first."]:["Fragile","Start with a starter emergency fund and a simple budget. Small steps compound fast."];
      var res=$("#quiz-result");res.style.display="block";
      set("quiz-score",score);set("quiz-band",band[0]);set("quiz-msg",band[1]);
      var ring=$("#quiz-ring");if(ring){ring.style.strokeDashoffset=String(326.7-326.7*score/100);}
      var fx=$("#quiz-fixes");if(fx)fx.innerHTML=weak.slice(0,3).map(function(w){var p=w.split("|");return '<li><a href="'+(PF.base||"")+p[1]+'">'+p[0]+'</a></li>';}).join("")||"<li>Keep going — review your plan once a year.</li>";
      var hid=$("#lead-score");if(hid)hid.value=score;
      PF.store.set("health_score",score);
    };
    var rs=$("#quiz-restart");if(rs)rs.addEventListener("click",function(){cur=0;$$("input",qz).forEach(function(i){i.checked=false;});$("#quiz-result").style.display="none";show(0);});
    show(0);
  }
})();
