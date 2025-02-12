import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RecipeService {
    private apiUrl = "http://localhost:5000/api/recipe";

    constructor(private http: HttpClient) {}

    getRecipe(payload: any): Observable<any> {
      return this.http.post<any>(this.apiUrl, payload);
    }
}
