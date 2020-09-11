```
python manage.py makemigrations
python manage.py migrate
```

## 更新muya的注意事项
1. dragDropCtrl.js要将

   ```js
   const nSrc = await this.muya.options.imageAction(path, id, name)
   ```

   改成

   ```js
   const nSrc = await this.muya.options.imageAction(image, id, name)
   ```
