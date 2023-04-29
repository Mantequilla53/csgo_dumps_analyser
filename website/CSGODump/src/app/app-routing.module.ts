import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TransactionGridComponent } from './transaction-grid/transaction-grid.component';
import { HomeComponent } from './home/home.component';
import { CommonModule } from '@angular/common';

const routes: Routes = [
  { path: '', component: HomeComponent},
  { path: 'transactions', component: TransactionGridComponent}
];

@NgModule({
  imports: [ CommonModule,
    RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
