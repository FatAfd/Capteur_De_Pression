/*** Graphical components binding ***/

// None in this app - all straightforward !

/*** Global Applications Constants ***/

let portOpened = false;
let port;




navigator.serial.addEventListener("disconnect", (event) => {
    port.close();
    portOpened = false;
});

let graphCreated = false;

/*** Application Functions ***/

async function onConnectButtonClick() {
    if (portOpened == false) {
        try {
            port = await navigator.serial.requestPort();
            await port.open({ baudRate: 115200 });
            portOpened = true;
            const reader = port.readable.getReader();
            let acc_buf = [];

            while (port.readable) {
                try {
                  while (true) {
                    const { value, done } = await reader.read();   // 2 valeurs qui viennent du read + await = asynchrone operator
                    if (done) {
                        // Allow the serial port to be closed later.
                        reader.releaseLock();
                        break;
                    }
                    if (value) {                                           // fonctionne si value est rempli ? 
                        acc_buf = new Uint8Array([...acc_buf,...value]);   //spread operator  --> ici équivalent à .append
                        let zeroIndex = acc_buf.indexOf(0);
                        if(zeroIndex != -1) {
                            let data = acc_buf.slice(0, zeroIndex + 1);     
                            message = decode(data).slice(0,-1);             // .slice enleve la dernière valeur de data decodé
                            try {
                                const data = proto.DataStream.deserializeBinary(message).toObject();
                                console.log(data);
                                if(data.valueList?.length == 36) {
                                    window.data.push(data.valueList);
                                    
                                    // const reshaped = Array(6).fill(0).map((e,i)=> data.valueList.slice(i*6,i*6+6));
                                    const transposed = Array(36).fill(0).map((e,i)=>6*(i%6)+Math.floor(i/6)).map(e=>data.valueList[e]);
                                     const reshaped = Array(6).fill(0).map((e,i)=> transposed.slice(i*6,i*6+6).reverse());
                                    if(!graphCreated) {
                                        graphCreated = true;
                                        Plotly.newPlot('graph', [{
                                            z: reshaped,
                                            type: 'heatmap',
                                        }], {
                                            width: 700,
                                            height: 700
                                        });
                                    }
                                    else {
                                        Plotly.restyle('graph', 'z', [reshaped]);
                                    }
                                    if(reshaped.every(row => row.every(value => value <= 8))){
                                        showErrorMessage("Les valeurs sont incorrectes. Veuillez vérifier le branchement.");
                                    }
                                }
                               
                                                            
                            } catch (error) {
                                console.error("Error while decoding message");
                                console.error(error);
                            }
                            acc_buf = [];
                        }
                    }
                  }
                } catch (error) {
                  console.error("Error while reading serial port");
                  console.error(error);
                }
            }
        }
        catch (err) {
            console.error("Error while opening serial port");
        }
    }
}

async function startMeasure() {
    if (portOpened == false) return;
    let request = new proto.Request();
    request.setStartmeasurements(new proto.StartMeasurements()); //voir à quoi ça ressemble en protobuff
    let protoMessage = request.serializeBinary();
    console.log(protoMessage)
    let cobsMessage = encode(protoMessage);
    console.log(cobsMessage)
    cobsMessage = new Uint8Array([...cobsMessage, 0]);
    console.log(cobsMessage)
    const writer = port.writable.getWriter();
    await writer.write(cobsMessage);
    writer.releaseLock();
    console.log("Start measure request sent");
    window.data = [];
   
   
   
    
}

async function stopMeasure() {
    if (portOpened == false) return;
    let request = new proto.Request();
    request.setStopmeasurements(new proto.StopMeasurements());
    let protoMessage = request.serializeBinary();
    let cobsMessage = encode(protoMessage);
    cobsMessage = new Uint8Array([...cobsMessage, 0]);
    const writer = port.writable.getWriter();
    await writer.write(cobsMessage);
    writer.releaseLock();
    console.log("Stop measure request sent");

    // Générer le contenu CSV avec des virgules comme séparateurs
    let csvContent = window.data.map(row => row.join(',')).join('\n');

    // Créer un élément <a> pour le téléchargement du fichier CSV
    const a = document.createElement('a');
    a.download = `${new Date().toISOString().split('.')[0].replace(/:/g,'.').replace('T',' ')}.csv`;
    
    // Créer un objet Blob à partir du contenu CSV
    const blob = new Blob([csvContent], { type: 'text/csv' });

    // Créer un URL pour le Blob
    const url = window.URL.createObjectURL(blob);
    
    // Assigner l'URL à l'élément <a>
    a.href = url;

    // Ajouter l'élément <a> au DOM
    document.body.appendChild(a);

    // Simuler un clic sur le lien pour démarrer le téléchargement
    a.click();

    // Supprimer l'élément <a> du DOM après le téléchargement
    document.body.removeChild(a);
}



  function showErrorMessage(message) {
    const errorMessageElement = document.getElementById('error-message');
    errorMessageElement.textContent = message;
    errorMessageElement.style.display = 'block';
  }

  











console.log("RUN JAVASCRIPT,  RUUUUUUUUNNNNN !!!!!");
