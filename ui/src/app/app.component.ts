import { Component, OnInit } from '@angular/core';
import { RecipeService } from './recipe.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  form: FormGroup;
  title = 'RecipeGenerator';
  recipe = "";
  recipeImage = "";
  isLoading = false;
  isValid = false;

  constructor(
    private recipeService: RecipeService,
    private fb: FormBuilder,
  ) {
    this.form = this.fb.group({
      ingredients: ["", Validators.required],
      restrictions: ["", Validators.required],
      type: ["", Validators.required],
      servings: ["", Validators.required]
    });
  }

  ngOnInit(): void{
    this.form.valueChanges.subscribe(value => {
      this.isValid = this.form.value.ingredients && this.form.value.restrictions && this.form.value.type && this.form.value.servings;
      this.recipe = "";
    })
  }

  getRecipe() {
    this.isLoading = true;
    this.recipeService.getRecipe(this.form.value).subscribe(
      (response) => {
        this.recipe = response.recipe;
        this.recipeImage = response.image;
        this.isLoading = false;
      },
      (error) => {
        console.error(error);
        this.isLoading = false;
      }
    );
  }
}
