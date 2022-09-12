import { Component, OnInit } from '@angular/core';
import { faUpload } from '@fortawesome/free-solid-svg-icons';
import { NgbOffcanvas } from '@ng-bootstrap/ng-bootstrap';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'CSGODump';
  trans: any[] = [];
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
    this.cases['totalContainers'] = this.trans.filter(x=> x.action == "Unlocked a container");
    this.cases['stickerCounts'] = this.cases['totalContainers'].filter((x: { taken: any[]; }) => {
      x.taken.some((y: { name: string; }) => /sticker|capsule/g.test(y.name.toLowerCase()))
    });
  }

}


