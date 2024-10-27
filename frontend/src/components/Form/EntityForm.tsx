// components/EntityForm.tsx
import React, { useState, ReactNode } from 'react';

type Field = {
  name: string;
  label: string;
  type: string;
};

type EntityFormProps = {
  fields: Field[];
  initialValues?: { [key: string]: any };
  onSubmit: (data: { [key: string]: any }) => void;
  buttonText?: string;
  children?: ReactNode;
};

const EntityForm: React.FC<EntityFormProps> = ({ fields, initialValues = {}, onSubmit, buttonText = "Submit", children }) => {
  const [formValues, setFormValues] = useState<{ [key: string]: any }>(initialValues);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormValues((prevValues) => ({
      ...prevValues,
      [name]: value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formValues);
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-lg mx-auto p-4 bg-white shadow-md rounded-md">
      {fields.map((field) => (
        <div key={field.name} className="mb-4">
          <label htmlFor={field.name} className="block text-gray-700 text-sm font-bold mb-2">
            {field.label}
          </label>
          <input
            type={field.type}
            name={field.name}
            id={field.name}
            value={formValues[field.name] || ''}
            onChange={handleChange}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
        </div>
      ))}
      <button
        type="submit"
        className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      >
        {buttonText}
      </button>
      {children}
    </form>
  );
};

export default EntityForm;
