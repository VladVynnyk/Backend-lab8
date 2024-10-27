// src/components/EntityForm.tsx
import React, { useState, useEffect } from 'react';

type Field = {
  name: string;
  label: string;
  type: string;
  options?: { label: string; value: string }[];
};

type EntityFormProps = {
  fields: Field[];
  initialValues?: { [key: string]: any };
  onSubmitSuccess: () => void;
  onCancel: () => void;
  entityName: string;
  id?: number;
  buttonText?: string;
};

const EntityForm: React.FC<EntityFormProps> = ({
  fields,
  initialValues = {},
  onSubmitSuccess,
  onCancel,
  entityName,
  id,
  buttonText = "Submit",
}) => {
  const [formValues, setFormValues] = useState<{ [key: string]: any }>(initialValues);
  const [categories, setCategories] = useState<{ label: string; value: string }[]>([]);
  const [isLoadingCategories, setIsLoadingCategories] = useState(false);

  useEffect(() => {
    if (entityName === "thermometers") {
      setIsLoadingCategories(true);
      fetch(import.meta.env.VITE_API_URL+'/categories')
        .then((res) => res.json())
        .then((data) => {
          const options = data.map((cat: { id: string; name: string }) => ({
            label: cat.name,
            value: cat.name,
          }));
          setCategories(options);
          setIsLoadingCategories(false);
        })
        .catch((error) => {
          console.error("Error fetching categories:", error);
          setIsLoadingCategories(false);
        });
    }
  }, [entityName]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormValues((prevValues) => ({
      ...prevValues,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData();
    Object.keys(formValues).forEach((key) => formData.append(key, formValues[key]));

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/${entityName}${id ? `/${id}` : ''}`, {
        method: id ? 'PUT' : 'POST',
        body: formData,
      });

      if (response.ok) {
        onSubmitSuccess();
      } else {
        console.error("Error submitting form:", await response.json());
      }
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-lg mx-auto p-4 bg-white shadow-md rounded-md">
      {fields.map((field) => (
        <div key={field.name} className="mb-4">
          <label htmlFor={field.name} className="block text-gray-700 text-sm font-bold mb-2">
            {field.label}
          </label>
          {field.name === "category" && entityName === "thermometers" ? (
            isLoadingCategories ? (
              <p>Loading categories...</p>
            ) : (
              <select
                name="category"
                id="category"
                value={formValues.category || ''}
                onChange={handleChange}
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              >
                <option value="">Select a Category</option>
                {categories.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            )
          ) : (
            <input
              type={field.type}
              name={field.name}
              id={field.name}
              value={formValues[field.name] || ''}
              onChange={handleChange}
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            />
          )}
        </div>
      ))}
      <div className="flex justify-between">
        <button
          type="submit"
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        >
          {buttonText}
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        >
          Cancel
        </button>
      </div>
    </form>
  );
};

export default EntityForm;
