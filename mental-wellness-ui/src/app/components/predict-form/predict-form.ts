import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Predict } from '../../services/predict';

@Component({
  selector: 'app-predict-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './predict-form.html',
  styleUrls: ['./predict-form.scss'],
})
export class PredictForm {
  wellnessForm: FormGroup;

  occupations = ['Employed', 'Student', 'Self-employed', 'Unemployed', 'Retired'];
  genders = ['Male', 'Female'];
  workModes = ['Remote', 'In-person', 'Hybrid'];

  result: number | null = null;
  loading = false;
  error: string | null = null;

  constructor(private fb: FormBuilder, private predictService: Predict) {
    this.wellnessForm = this.fb.group({
      age: [null, Validators.required],
      gender: ['', Validators.required],
      occupation: ['', Validators.required],
      work_mode: ['', Validators.required],

      screen_time_hours: [null, Validators.required],
      work_screen_hours: [null, Validators.required],
      leisure_screen_hours: [null, Validators.required],

      sleep_hours: [null, Validators.required],
      sleep_quality_1_5: [null, [Validators.required, Validators.min(1), Validators.max(5)]],

      stress_level_0_10: [null, [Validators.required, Validators.min(0), Validators.max(10)]],
      productivity_0_100: [null, [Validators.required, Validators.min(0), Validators.max(100)]],

      exercise_minutes_per_week: [null, Validators.required],
      social_hours_per_week: [null, Validators.required],
    });
  }

  submit() {
    if (this.wellnessForm.invalid) return;

    this.loading = true;
    this.error = null;
    this.result = null;

    const payload = this.wellnessForm.value;

    this.predictService.predict(payload).subscribe({
      next: (res) => {
        this.result = res.mental_wellness_index;
        this.loading = false;
      },
      error: () => {
        this.error = 'Failed to get prediction';
        this.loading = false;
      },
    });
  }
}
