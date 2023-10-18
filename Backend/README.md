## Backend Application for Airsight Platform

### Create the Virtual Environment
To create the virtual environment, run the following command:
```markdown
```powershell
py -m venv venv
```

### Activate the Virtual Environment
Activate the virtual environment with the following command:
```powershell
./venv/Scripts/activate
```

**NOTE**: If you encounter execution policy errors on Windows, you may need to update the necessary policies. Here are the steps to do so:

1. Open Windows PowerShell as an administrator.

2. Set the execution policy to `RemoteSigned` using the following command:
   ```powershell
   Set-ExecutionPolicy RemoteSigned
   ```

### Install Required Packages
Install the packages listed in `requirements.txt` using pip:
```powershell
py -m pip install -r requirements.txt
```

### Freeze Installed Packages
To freeze the installed packages and update the `requirements.txt` file, use the following command:
```powershell
py -m pip freeze > requirements.txt
```
