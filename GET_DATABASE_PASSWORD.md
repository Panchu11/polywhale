# 🔑 How to Get Your Supabase Database Password

You need this password to complete the setup. Here are 3 easy ways to get it:

---

## 🎯 Method 1: Check Your Email (Easiest)

When you created the Supabase project, you should have received an email with the password.

1. Open your email
2. Search for "Supabase" or "polywhale"
3. Look for the project creation email
4. Copy the password

---

## 🎯 Method 2: Get Connection String from Supabase

### Step-by-Step:

1. **Go to Supabase Dashboard**
   - Open: https://supabase.com/dashboard/project/hkcdmrhamilgukuyfigd/settings/database
   - Log in if needed

2. **Find Connection String**
   - Scroll down to **"Connection string"** section
   - Click the **"URI"** tab (not "Session mode" or "Transaction mode")

3. **Copy the String**
   - You'll see something like:
     ```
     postgresql://postgres.hkcdmrhamilgukuyfigd:abc123xyz@aws-0-us-east-1.pooler.supabase.com:6543/postgres
     ```
   - The password is the part between `:` and `@`
   - In the example above, the password is: `abc123xyz`

4. **Use the Full String**
   - Or just copy the entire connection string
   - Paste it into your `.env` file as `DATABASE_URL`

---

## 🎯 Method 3: Reset Password (If You Forgot)

### Step-by-Step:

1. **Go to Database Settings**
   - Open: https://supabase.com/dashboard/project/hkcdmrhamilgukuyfigd/settings/database

2. **Reset Password**
   - Scroll down to **"Database password"** section
   - Click **"Reset database password"**
   - Click **"Generate new password"**

3. **Copy New Password**
   - Supabase will show you the new password
   - **IMPORTANT**: Copy it immediately (you won't see it again!)
   - Save it somewhere safe

4. **Update .env File**
   - Open `.env` file in your project
   - Replace `[YOUR-PASSWORD]` with the new password
   - Save the file

---

## 📝 Where to Put the Password

### Option A: Use Full Connection String

1. Copy the entire connection string from Supabase
2. Open `.env` file
3. Replace this line:
   ```
   DATABASE_URL=postgresql://postgres.hkcdmrhamilgukuyfigd:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```
   With the full string from Supabase:
   ```
   DATABASE_URL=postgresql://postgres.hkcdmrhamilgukuyfigd:your_actual_password@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```

### Option B: Just Replace the Password

1. Open `.env` file
2. Find this line:
   ```
   DATABASE_URL=postgresql://postgres.hkcdmrhamilgukuyfigd:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```
3. Replace `[YOUR-PASSWORD]` with your actual password:
   ```
   DATABASE_URL=postgresql://postgres.hkcdmrhamilgukuyfigd:abc123xyz@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```
4. Save the file

---

## ✅ Verify It Works

After updating the `.env` file:

1. Open Command Prompt
2. Navigate to project:
   ```bash
   cd c:\Users\panchu\Desktop\polywhales
   ```
3. Activate virtual environment:
   ```bash
   venv\Scripts\activate
   ```
4. Test database connection:
   ```bash
   python scripts\test_db.py
   ```

**If you see "✓ Database connected" - SUCCESS!**

**If you see an error - the password is wrong, try again**

---

## 🔒 Security Tips

1. **Never share your database password**
2. **Never commit `.env` file to GitHub** (it's already in `.gitignore`)
3. **Save the password in a password manager**
4. **Rotate password every 3-6 months**

---

## 🆘 Still Having Issues?

### Error: "password authentication failed"
- The password is incorrect
- Try resetting it (Method 3 above)

### Error: "could not connect to server"
- Check your internet connection
- Verify the Supabase project is active
- Try the alternative connection string in `.env` file (see the commented line)

### Error: "database does not exist"
- The connection string is wrong
- Make sure you're using the correct project ID: `hkcdmrhamilgukuyfigd`

---

## 📞 Quick Links

- **Database Settings**: https://supabase.com/dashboard/project/hkcdmrhamilgukuyfigd/settings/database
- **Supabase Dashboard**: https://supabase.com/dashboard/project/hkcdmrhamilgukuyfigd
- **Supabase Docs**: https://supabase.com/docs

---

## 🎯 Next Steps After Getting Password

1. ✅ Update `.env` file with password
2. ✅ Run `python scripts\init_db.py`
3. ✅ Run `python scripts\test_db.py`
4. ✅ Run `python main.py`
5. ✅ Test bot in Telegram

---

**You're almost there! Just get that password and you're done! 🚀**

