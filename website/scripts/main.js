function AppViewModel() {
    self = this;
    self.transactions = ko.observableArray([]);

    function onReaderLoad(event) {
        console.log(event.target.result);
        this.fileJson = JSON.parse(event.target.result);
    }
}

function fileSelected(event) {
    var reader = new FileReader();
    reader.onload = onReaderLoad;
    reader.readAsText(event.target.files[0])
}


ko.applyBindings(new AppViewModel());