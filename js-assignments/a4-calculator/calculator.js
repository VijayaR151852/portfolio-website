//Write your javascript logic here

// function getExpressionOutput(input) {
//   try {
//     return eval(input);
//   }
//   catch (e) {
//     console.warn('Invalid expression', input)
//     return input
//   }
// }

// function onClickShowOutput() {
//   let expression = '5+2*10'
//   const output = getExpressionOutput(expression)
//   console.log(output)
//   document.getElementById('output').innerHTML = output;
// }

function cal(val) {
  document.getElementById("result").value += val;
}

function solve() {
  let resExp = document.getElementById("result").value;
  let res;
  try {
    res= eval(resExp);
    }
    catch (e) {
      console.warn('Invalid expression', resExp)
      res="Invalid";
    }
  document.getElementById("result").value = res;
}

function clr(val) {
  if(val=="c"){
    let res;
    let str=document.getElementById("result").value;
    res=str.slice(0,-1);
    document.getElementById("result").value = res;
  }
  else{
    document.getElementById("result").value = "0";
  }
}

// alert(null===undefined)
alert(Symbol("hello")=="hhh")