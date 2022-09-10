import { Component, OnInit } from '@angular/core';
import {ScrollingModule} from '@angular/cdk/scrolling';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'CSGODump';
  trans: any[] = [];

  constructor() {};

  ngOnInit(): void {
  }

  fileSelected(event : any) {
    var reader = new FileReader();
    reader.onload = (e: any) => {
      this.trans = JSON.parse(e.target.result);
    };
    reader.readAsText(event.target.files[0])
  };



  formatIcon(url: any): string {
    return "https://community.steamstatic.com/economy/image/" + url
  }
}


