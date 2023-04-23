import { Component, OnInit } from '@angular/core';
import { faUpload } from '@fortawesome/free-solid-svg-icons';
import { NgbOffcanvas } from '@ng-bootstrap/ng-bootstrap';
import { Constants } from './models/constants';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'CSGODump';
  trans: any[] = [];
  containers: any[] = [];
  cases: any = {};
  faUpload = faUpload;
  closeResult = '';

  constructor(private offCanvasService: NgbOffcanvas) {};

  ngOnInit(): void {}

  open(content : any) {
    this.offCanvasService.open(content, {ariaLabelledBy: 'offcanvas-basic-title'}).result;
  }

  onDragOver(event : any){
    event.preventDefault();
  }
  onDropSuccess(event : any){
    event.preventDefault();
    this.fileChanged(event.dataTransfer.files[0]);
  }
  fileSelected(event : any) {
    this.fileChanged(event.target.files[0])
  };
  fileChanged(file : File){
    var reader = new FileReader();
    reader.onload = (e: any) => {
      this.trans = JSON.parse(e.target.result);
      this.setupData()
    };
    reader.readAsText(file)
  }

  formatIcon(url: any): string {
    return "https://community.steamstatic.com/economy/image/" + url
  }
  setupData() : void{
    this.containers = this.trans.filter(x=> x.action == "Unlocked a container");
    this.cases['all'] = this.containers.filter(transaction => transaction.taken.some(s=> s.name.includes("Case"))).flatMap(x=> x.given);
    this.cases['golds'] = this.cases['all'].filter(x=> Constants.Golds.some(t => x.type.includes(t)));
    this.cases['reds'] = this.cases['all'].filter(x=> Constants.Reds.some(t => x.type.includes(t) && !x.type.includes("★")));
    this.cases['pinks'] = this.cases['all'].filter(x=> Constants.Pinks.some(t => x.type.includes(t)));
    this.cases['purples'] = this.cases['all'].filter(x=> Constants.Purples.some(t => x.type.includes(t)));
    this.cases['blues'] = this.cases['all'].filter(x=> Constants.Blues.some(t => x.type.includes(t)));
    this.cases['lightBlues'] = this.cases['all'].filter(x=> Constants.LightBlues.some(t => x.type.includes(t)));
  }

}


