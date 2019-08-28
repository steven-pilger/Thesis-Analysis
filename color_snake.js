// helper function to download the not_colored data to file
function download(content, fileName, contentType) {
   var a = document.createElement("a");
   var file = new Blob([content], {type: contentType});
   a.href = URL.createObjectURL(file);
   a.download = fileName;
   a.click();
}
let not_colored;

$.getScript("https://d3js.org/d3.v5.min.js", () => {
    // dictionary of feature codes and their associated colors plus catch variable
    const scale = {
       HY: { bg_color: "#93d050" },
       HA: { bg_color: "#ffff00" },
       M: { bg_color: "#ffff00" },
       A: { bg_color: "#ffff00" },
       I: { bg_color: "#ffff00" },
       L: { bg_color: "#ffff00" },
       V: { bg_color: "#ffff00" },
       HR: { bg_color: "#07b050" },
       W: { bg_color: "#07b050" },
       Y: { bg_color: "#07b050" },
       F: { bg_color: "#07b050" },
       Hb: { bg_color: "#7030a0", font_color: "#ffffff" },
       N: { bg_color: "#7030a0", font_color: "#ffffff" },
       Q: { bg_color: "#7030a0", font_color: "#ffffff" },
       S: { bg_color: "#7030a0", font_color: "#ffffff" },
       T: { bg_color: "#7030a0", font_color: "#ffffff" },
       Hu: { bg_color: "#7030a0", font_color: "#ffffff" },
       Ha: { bg_color: "#7030a0", font_color: "#ff0000" },
       Hd: { bg_color: "#7030a0", font_color: "#02b0f0" },
       "+-": { bg_color: "#0070c0", font_color: "#ff0000" },
       "+": { bg_color: "#0070c0", font_color: "#000000" },
       H: { bg_color: "#0070c0", font_color: "#000000" },
       K: { bg_color: "#0070c0", font_color: "#000000" },
       R: { bg_color: "#0070c0", font_color: "#000000" },
       "-": { bg_color: "#ff0000" },
       D: { bg_color: "#ff0000" },
       E: { bg_color: "#ff0000" },
       Sm: { bg_color: "#ffffff" },
       aH: { bg_color: "#d9d9d9" },
       G: { bg_color: "#ff02ff" },
       P: { bg_color: "#d603ff", font_color: "#ffffff" },
       C: { bg_color: "#bf8f00" }
    };

    // select all circles and set their generic number as class
    d3.select('svg#snakeplot').selectAll('circle').each(function(d){
       let curr = d3.select(this)
       let gn = curr.attr('original_title')

       let gn_data = gn.split(' ')
       if (gn_data.length === 3) {
          // let gn_clean = gn_data[2].replace('.', 'x')
          let gn_clean = gn_data[2].split(/\.\d{2}/).join('')
          curr.classed('g' + gn_clean, true)
       }
    })

    // coloring circles according to json data
    not_colored = []
    for (let entry of data) {
       let gn_clean = 'g' + entry['gn'].replace('.', 'x')
       let code = entry['code'].replace('α', 'a')
       let color = scale[code]['bg_color']
       let selector = 'circle.' + gn_clean

       let selection = d3.select(selector)
       if ( !selection.empty() ) {
          selection.style('fill', color)
       } else {
          not_colored.push(entry)
       }
    }
    download(not_colored, 'json.txt', 'text/plain');         
});